#Step 1: Preprocessing the Data

import pandas as pd

# Load the dataset
df = pd.read_csv("your_dataset.csv")

# Create lists of texts and summaries
texts = df["text"].tolist()
summaries = df["summary"].tolist()


#Step 2: Creating a Tokenizer
from transformers import BartTokenizer

# Load the BART tokenizer
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")

# Tokenize the texts and the summaries
inputs = tokenizer(texts, truncation=True, max_length=512, padding="max_length", return_tensors="pt")
labels = tokenizer(summaries, truncation=True, max_length=128, padding="max_length", return_tensors="pt")

#Step 3: Preparing the Dataset
from torch.utils.data import Dataset

class SummaryDataset(Dataset):
    def __init__(self, inputs, labels):
        self.inputs = inputs
        self.labels = labels

    def __len__(self):
        return len(self.inputs["input_ids"])

    def __getitem__(self, idx):
        return {key: tensor[idx] for key, tensor in self.inputs.items()}, self.labels["input_ids"][idx]

dataset = SummaryDataset(inputs, labels)

#Step 4: Creating the Model

from transformers import BartForConditionalGeneration

model = BartForConditionalGeneration.from_pretrained("facebook/bart-large")

#Step 5: Training the Model

from transformers import Trainer, TrainingArguments

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=2,
    per_device_train_batch_size=16,
    gradient_accumulation_steps=2,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
)

# Create the trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

# Train the model
trainer.train()
