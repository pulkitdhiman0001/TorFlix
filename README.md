# TorFlix

**TorFlix** is a Flask-based web application that allows users to download movies, TV shows, documentaries, anime, music, and more. This README will guide you through the process of setting up and running the **TorFlix** project on your local machine.

## Prerequisites

Before getting started, ensure that you meet the following prerequisites:

- [Python](https://www.python.org/downloads/) (3.x) installed on your system.
- The following packages must be installed based on your operating system:
  - **lame** for audio conversion:
    - **Windows**: Download 'lame' from [lame.sourceforge.net](http://lame.sourceforge.net/) and follow the installation instructions.
    - **Ubuntu/Debian**:
      ```bash
      sudo apt-get install lame
      ```
    - **Red Hat (Fedora, CentOS)**:
      ```bash
      sudo yum install lame
      ```
    - **macOS**:
      ```bash
      brew install lame
      ```
  - **ffmpeg** for multimedia processing:
    - **Windows**: Download 'ffmpeg' from [ffmpeg.org](https://www.ffmpeg.org/download.html) and follow the installation instructions.
    - **Ubuntu/Debian**:
      ```bash
      sudo apt-get install ffmpeg
      ```
    - **Red Hat (Fedora, CentOS)**:
      ```bash
      sudo yum install ffmpeg
      ```
    - **macOS**:
      ```bash
      brew install ffmpeg
      ```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/pulkitdhiman0001/TorFlix.git
   ```

2. Navigate to the project directory:

   ```bash
   cd TorFlix
   ```

3. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install the 'lame' package for audio conversion:

  - **Windows**: Download 'lame' from [lame.sourceforge.net](http://lame.sourceforge.net/) and follow the installation instructions.
    - **Ubuntu/Debian**:
      ```bash
      sudo apt-get install lame
      ```
    - **Red Hat (Fedora, CentOS)**:
      ```bash
      sudo yum install lame
      ```
    - **macOS**:
      ```bash
      brew install lame
      ```
5. Install the 'ffmpeg' package for multimedia processing:

    - **Windows**: Download 'ffmpeg' from [ffmpeg.org](https://www.ffmpeg.org/download.html) and follow the installation instructions.
    - **Ubuntu/Debian**:
      ```bash
      sudo apt-get install ffmpeg
      ```
    - **Red Hat (Fedora, CentOS)**:
      ```bash
      sudo yum install ffmpeg
      ```
    - **macOS**:
      ```bash
      brew install ffmpeg
      ```
## Libtorret Fix (Optional. If you are facing issues in installation of libtorrent):
   ** If you are getting error such as "module not found 'libtorrent' or not able to install or build the libtorrent library. Then you can do this process manually by following the below steps." **
  - Fist install all the packages using requirements.txt
  - open the terminal and install the libtorrent system-wide library using the following command (skip if already done):
    ```bash
    sudo apt install python3-libtorrent
    ```
  - Now get the installation path of the system-wide libtorrent you just installed:
      - open the new terminal and type 'python3 shell'
      - then type the following code to get the system-wide libtorrent path:
        ``` bash
        import sys
        print(sys.path)
        ```
  - Next we need to make a bridge between the system-wide libtorrent and your project virtual environment. you can do this by using the following command:
``` bash
ln -s /the/path/you/got/using the print(sys.path) command your_virtual_env_path/lib/python3.11/site-packages/libtorrent.cpython-311-x86_64-linux-gnu.so
```
  -Example:
``` bash
ln -s /usr/lib/python3/dist-packages/libtorrent.cpython-311-x86_64-linux-gnu.so /home/anon/PycharmProjects/torflix-sample/venv/lib/python3.11/site-packages/libtorrent.cpython-311-x86_64-linux-gnu.so
```
- This should fix all your problems with libtorrent.

## Usage

1. Start the Flask application:

   ```bash
   python app.py
   ```

2. Access the application in your web browser at http://localhost:5000.

3. Search for movies, TV shows, music, or other content, and follow the on-screen instructions to download.

## Screenshots

1. Home Page
![1](https://github.com/pulkitdhiman0001/TorFlix/assets/115160739/079cffea-9b80-48b8-a1fc-4c89f59f84bb)

2. Selecting a Torrent
![2](https://github.com/pulkitdhiman0001/TorFlix/assets/115160739/5869fb7f-dc7f-49de-ab5a-74b8204af926)

3. User Login Page
![3](https://github.com/pulkitdhiman0001/TorFlix/assets/115160739/7a4f4414-660c-4324-a244-1570c1d89332)

4. Home page after Login
![4](https://github.com/pulkitdhiman0001/TorFlix/assets/115160739/f0386f41-7105-4037-914f-78a2622272ab)

5. Opening a Torrent after Login-in
![5](https://github.com/pulkitdhiman0001/TorFlix/assets/115160739/5a9bb6cc-1bfc-47df-b79b-c0f7df822980)

6. Downloading a Torrent
![6](https://github.com/pulkitdhiman0001/TorFlix/assets/115160739/685f10d0-9470-4f65-8084-70e40151e6c3)

7. List of global torrent download in progress
![7](https://github.com/pulkitdhiman0001/TorFlix/assets/115160739/16544eed-2b6f-48f5-85c7-09ba342a262a)

8. List of global torrent download history
![8](https://github.com/pulkitdhiman0001/TorFlix/assets/115160739/3809898c-a441-4ef6-89b8-5dfcbc86a1e2)

9. User my_list (Torrents Downloaded by user)
![9](https://github.com/pulkitdhiman0001/TorFlix/assets/115160739/41d96fda-b642-4516-b8e0-1e76e19428b4)

10. Actions the owner(User who downloaded the torrent) of torrent can perform
![Screenshot from 2023-10-02 19-08-03](https://github.com/pulkitdhiman0001/TorFlix/assets/115160739/85a7cd25-bddb-4118-a80a-c4a95b19d290)

11. Global downloads (Torrents Downloaded by other users including logged-in user)
![10](https://github.com/pulkitdhiman0001/TorFlix/assets/115160739/7847e59d-1eaa-4df8-9adc-4726516a8ad7)

