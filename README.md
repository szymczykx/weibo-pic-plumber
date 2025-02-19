# Weibo Pic Plumber

A tool for rescuing recently deleted Weibo images using CDN cache.

## Features

- Retrieves deleted Weibo images from CDN cache
- Updates CDN server list automatically
- Supports multiple DNS resolvers worldwide
- Progress bar visualization for operations
- Multiple image URLs processing in one command

## Requirements

- Python 3.7+
- Required packages:
  - dnspython
  - requests
  - tqdm
  - argparse

## Installation

1. Clone the repository:
```bash
git clone https://github.com/szymczykx/weibo-pic-plumber.git
cd weibo-pic-plumber
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Update CDN Server List

```bash
python PicPlumber.py --updatecdn
```

### Download Images

Single image:
```bash
python PicPlumber.py https://wx1.sinaimg.cn/large/example.jpg
```

Multiple images:
```bash
python PicPlumber.py https://wx1.sinaimg.cn/large/example1.jpg https://wx2.sinaimg.cn/large/example2.jpg
```

## How It Works

1. The tool maintains a list of Weibo CDN domains and DNS servers
2. When updating CDN info, it queries multiple DNS servers to get IP addresses for each CDN domain
3. When downloading an image, it tries different CDN IPs until finding a working cache
4. The tool uses custom headers to simulate browser requests

## Note

- This tool only works for recently deleted images that are still in CDN cache
- Success rate depends on how long ago the image was deleted
- Some CDN nodes might be slower or unreachable depending on your location

## License

MIT License

## Contributing

Feel free to open issues or pull requests for any improvements.
