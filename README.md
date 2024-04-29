# Felix

## Introduction

Felix is an application designed to automatically generate proposal rationales and comments for specified `enriched_proposal_ids` from the Evooq Montblanc database, simplifying the analysis and enhancement of financial proposals.

## Prerequisites

- **MariaDB**: Installed and running with the Evooq Montblanc database set up.

- **Python 3**: Version 3.6 or newer.

## Installation

- **Database Setup**: Ensure MariaDB contains the Montblanc database.
- **Clone Felix**: `git clone https://github.com/yokurang/felix`.
- **Install Dependencies**: In the Felix directory, run `pip install -r requirements.txt`.

## Usage

Run `python main.py` and input the `enriched_proposal_id` when prompted to receive generated insights.

## Logs

Logs from running the application can be found in the `logs` folder.
