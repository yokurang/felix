# Felix

## Introduction

Felix is an automated tool designed to generate proposal rationales and comments for specific `enriched_proposal_ids` from the Evooq Montblanc database. This simplifies the process of analyzing and enhancing financial proposals by providing actionable insights and data-driven feedback.

## Prerequisites

- **MariaDB**: Must be installed and actively running with the Evooq Montblanc database properly configured.
- **Python 3**: Required version is 3.6 or newer.

## Installation

### Clone the Repository

```bash
git clone https://github.com/yokurang/felix
cd felix
```

### Database Setup

Ensure that MariaDB is configured with the Montblanc database. Import the initial dataset if necessary:

```bash
mysql -u username -p database_name < path/to/montblanc-0500.sql
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

To run Felix, execute the main script and follow the on-screen prompts to input the `enriched_proposal_id`:

```bash
python main.py
```

## Features

- **GPT Handler**: Interfaces with the OpenAI API to fetch and generate text based on predefined prompts.
- **DB Handler**: Manages connections and interactions with the MariaDB database, ensuring data is fetched and stored correctly.

## Logs

Logs are generated during execution and can be found in the `logs` directory for debugging and tracking application performance.

## Project Structure

```plaintext
.
├── README.md
├── __pycache__
│   ├── commands.cpython-311.pyc
│   ├── db_handler.cpython-311.pyc
│   ├── gpt_handler.cpython-311.pyc
│   └── telebot.cpython-311.pyc
├── application.log
├── commands.py
├── data
│   ├── all_enriched_proposal_details.json
│   └── montblanc-0500.sql
├── db_handler.py
├── gpt_handler.py
├── logs
│   └── db_handler.log
├── main.py
├── p2r
│   ├── instructor_template.ipynb
│   ├── main.py
│   └── tables_557.py
├── requirements.txt
└── test_gpt.py
```

## Future Developments

- **Market and Macro Data**: Integration of a vector database for market and macro data, enabling the LLM to query this database based on stock information to provide justifications.
- See the Google Collab notebook for a proof of concept regarding this integration.

## Contributing

Contributions to Felix are welcome! Please feel free to fork the repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

Ensure to update tests as appropriate.

## License

Specify the license under which the project is released.


