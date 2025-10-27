# Irys Testnet Automation Bot

A comprehensive automation bot for interacting with the Irys testnet. This bot enables automated operations including token requests from faucets, game balance management, playing games, NFT minting, and proxy management.

## Features

- 🔑 **Request Tokens from Faucet** - Automated token requests with captcha solving
- 💎 **Top Up Game Balance** - Deposit IRYS tokens to game contracts
- 🎮 **Play Games** - Automated gameplay for multiple arcade games
- 📥 **Mint NFTs** - Mint NFTs from Irys OmniHub
- 📦 **All-in-One Module** - Execute multiple operations in sequence
- 🔄 **Proxy Management** - Automatic proxy rotation and management
- 🛡️ **Error Handling** - Robust error handling with automatic retries
- 📊 **Progress Tracking** - Real-time progress monitoring and result logging
- 🗄️ **Database Integration** - SQLite/PostgreSQL database for account management

## Supported Operations

### 1. Request Tokens from Faucet
Automatically requests testnet tokens from the Irys faucet with captcha solving.

### 2. Top Up Game Balance
Deposits IRYS tokens into game smart contracts to enable gameplay.

### 3. Play Games
Plays various arcade games on the Irys platform:
- Snake
- Asteroids
- Hex Shooter
- Missile Command
- Spritetype

### 4. Mint OmniHub NFT
Mints NFTs from the Irys OmniHub platform.

### 5. All-in-One Module
Executes a sequence of operations:
- Request from faucet
- Wait for balance
- Top up game balance
- Play games
- Mint NFTs

## Prerequisites

- Python 3.8 or higher
- Windows, Linux, or macOS
- Internet connection
- Captcha solving service API key (optional)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Irys_Testnet
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the application

Edit `config/settings.yaml` to configure:

- **Application Settings**: Thread count, database URL, proxy settings
- **Delay Settings**: Customize delays between operations
- **Captcha Settings**: Configure your preferred captcha solver
- **Game Settings**: Set game parameters and amounts
- **Web3 Settings**: Configure RPC endpoints

### 4. Prepare account files

Add your accounts to the following files in `config/data/`:

- `all_in_one_accounts.txt` - Accounts for all-in-one operations
- `mint_nft_accounts.txt` - Accounts for NFT minting
- `play_games_accounts.txt` - Accounts for playing games
- `top_up_game_balance_accounts.txt` - Accounts for topping up game balance
- `request_tokens_accounts.txt` - Accounts for requesting tokens
- `proxies.txt` - Proxy list (optional)

#### Account File Format
```
private_key:proxy (optional)
private_key:proxy (optional)
```

## Configuration

### Settings.yaml

The main configuration file is located at `config/settings.yaml`:

```yaml
application_settings:
  threads: 10                              # Number of concurrent threads
  database_url: "sqlite://./database.sqlite3"
  shuffle_accounts: true                    # Shuffle accounts before execution
  check_uniqueness_of_proxies: true        # Check for duplicate proxies
  disable_auto_proxy_change: false         # Disable automatic proxy rotation

attempts_and_delay_settings:
  delay_before_start:
    min: 0                                  # Random delay before starting (seconds)
    max: 0
  delay_between_games:
    min: 10                                 # Delay between games (seconds)
    max: 15
  delay_for_game:
    min: 10                                 # How long to "play" each game (seconds)
    max: 15
  delay_between_tasks:
    min: 10                                 # Delay between tasks in all-in-one (seconds)
    max: 20
  error_delay: 10                          # Delay on error (seconds)
  max_faucet_attempts: 5                   # Maximum faucet request attempts
  max_captcha_attempts: 5                  # Maximum captcha solving attempts
  max_games_attempts: 3                    # Maximum game attempts
  max_nft_mint_attempts: 3                 # Maximum NFT mint attempts
  max_tasks_attempts: 3                    # Maximum task attempts

captcha_settings:
  captcha_solver: "capsolver"              # Options: 2captcha, anti_captcha, capsolver, solvium
  max_captcha_solving_time: 60
  solvium_captcha_api_key: ""
  two_captcha_api_key: ""
  anti_captcha_api_key: ""
  capsolver_api_key: "CAP-"
  capmonster_api_key: ""

all_in_one_settings:
  tasks_to_perform:
    - "faucet"
    - "wait_for_balance"
    - "top_up_game_balance"
    - "play_games"
    - "mint_omnihub_nft"

games_settings:
  top_up_amount:
    min: 0.0015                             # Amount to top up (IRYS)
    max: 0.0020
  games_to_play:
    - "snake"
    - "asteroids"
    - "hex-shooter"
    - "missile-command"
    - "spritetype"

web3_settings:
  verify_balance: true                      # Verify balance before operations
  irys_rpc_url: "https://testnet-rpc.irys.xyz/v1/execution-rpc"
```

## Usage

### Running the Bot

```bash
python main.py
```

### Interactive Console

The bot features an interactive console interface:

```
✨ IRYS Bot 1.0 ✨
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 All in One
🔑 Request tokens from faucet
💎 Top up game balance
🎮 Play games
📥 Mint OmniHub NFT
🧹 Clean accounts proxies
❌ Exit
```

### Module Selection

Choose a module from the interactive menu:
1. **All in One** - Execute all operations in sequence
2. **Request tokens from faucet** - Request testnet tokens
3. **Top up game balance** - Deposit tokens to games
4. **Play games** - Automate gameplay
5. **Mint OmniHub NFT** - Mint NFTs
6. **Clean accounts proxies** - Clear proxy assignments
7. **Exit** - Close the application

## Results

Results are automatically saved to the `results/` directory:

- `all_in_one/` - All-in-one operation results
- `mint_nft/` - NFT minting results
- `play_games/` - Gameplay results
- `request_tokens/` - Faucet request results
- `top_up_game_balance/` - Balance top-up results

Each module creates:
- `*_success.txt` - Successful operations
- `*_failed.txt` - Failed operations

## Database

The bot uses a SQLite database (`database.sqlite3`) to store:
- Wallet addresses
- Private keys (encrypted)
- Active proxy assignments

To use PostgreSQL instead, update the `database_url` in `settings.yaml`:
```yaml
database_url: "postgres://user:password@localhost/dbname"
```

## Proxy Management

Proxies are automatically managed and rotated:
- Loaded from `config/data/proxies.txt`
- Assigned to accounts dynamically
- Automatically changed on errors (unless disabled)
- Unique proxy enforcement

### Proxy Format
```
http://user:pass@host:port
socks5://user:pass@host:port
```

## Captcha Solving

The bot supports multiple captcha solving services:
- **CapSolver** (default)
- **2Captcha**
- **Anti-Captcha**
- **Solvium**
- **Capmonster**

Configure your preferred service in `settings.yaml`.

## Logging

Logs are stored in the `logs/` directory with timestamps:
```
logs/main_2025-10-27_09-43-39.log
```

Logs include:
- Operation progress
- Success/failure status
- Error messages
- Transaction details

## Project Structure

```
Irys_Testnet/
├── config/
│   ├── data/                    # Account and proxy files
│   └── settings.yaml            # Configuration file
├── core/
│   ├── api/                     # API integrations
│   ├── bot/                     # Bot logic
│   ├── captcha/                 # Captcha solvers
│   ├── exceptions/              # Error handling
│   ├── modules/                 # Module executor
│   └── onchain/                 # Blockchain interactions
├── database/
│   └── models/                  # Database models
├── utils/                       # Utility functions
├── results/                     # Result files
├── logs/                        # Log files
├── main.py                      # Entry point
└── requirements.txt             # Dependencies
```

## Dependencies

Key dependencies:
- `web3` - Ethereum interaction
- `eth-account` - Wallet management
- `httpx` - HTTP client
- `loguru` - Logging
- `tortoise-orm` - Database ORM
- `inquirer` - Interactive console
- `rich` - Terminal formatting

## Troubleshooting

### Common Issues

**1. Import Errors**
```bash
pip install -r requirements.txt
```

**2. Database Errors**
- Ensure SQLite database has proper permissions
- Check database connection string

**3. Proxy Errors**
- Verify proxy format
- Check proxy connectivity
- Disable proxy auto-change if needed

**4. Captcha Errors**
- Verify API key
- Check API credit balance
- Try a different captcha solver

**5. Transaction Errors**
- Verify RPC endpoint
- Check account balances
- Verify network connectivity

## Security

⚠️ **Important Security Notes:**
- Never commit private keys to version control
- Store private keys securely
- Use proxies to protect your accounts
- Regularly rotate proxies
- Keep API keys secure

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Disclaimer

This bot is for educational purposes only. Users are responsible for their actions. Always comply with terms of service and local regulations.

## Support

- GitHub: https://github.com/Crazyscholarr
- Telegram: https://t.me/@Crazyscholarr

---

**Powered by CrazyScholar** 🚀

