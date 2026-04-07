import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from pathlib import Path
import pickle


def load_data(
        file_path: str,
        batch_size: int = 64,
        shuffle: bool = True,
        device: str = 'cpu'
) -> DataLoader:
    with open(file_path, 'rb') as f:
        data = pickle.load(f)

    state = torch.tensor(data['X'], dtype=torch.float32, device=device).squeeze(1)
    action = torch.tensor(data['y'], dtype=torch.float32, device=device).squeeze(1)

    dataset = TensorDataset(state, action)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

    return dataloader


def main():
    file_dir = Path(__file__).resolve().parent
    demo_path = file_dir / "demos.pkl"
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device is {device}")
    dataloader = load_data(demo_path, device=device)

    model = nn.Sequential(
        nn.Linear(14, 64),
        nn.ReLU(),
        nn.Linear(64, 64),
        nn.ReLU(),
        nn.Linear(64, 7)
    ).to(device)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(500):
        total_loss = 0
        for state, action in dataloader:
            pred = model(state)
            loss = criterion(pred, action)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        if (epoch + 1) % 50 == 0:
            print(f"Epoch {epoch+1}/500, Loss: {total_loss / len(dataloader):.4f}")

    torch.save(model, file_dir / "imitation_policy.pt")
    print("Saved imitation_policy.pt")


if __name__ == "__main__":
    main()
