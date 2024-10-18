# Server Setup and FastAPI Deployment Guide

## 1. VSCode Setup

1. Install the "Remote - SSH" extension in VSCode
2. Install the "Python" extension in VSCode
3. Open a folder using Remote - SSH

## 2. Secure Your Server

### Disable Root Access

1. Create a new user:
   ```
   adduser newusername
   ```

2. Grant sudo privileges to the new user:
   ```
   usermod -aG sudo newusername
   ```

3. Edit the SSH configuration:
   ```
   sudo nano /etc/ssh/sshd_config
   ```

4. Locate the line `PermitRootLogin yes` and change it to:
   ```
   PermitRootLogin no
   ```

5. Save and exit the editor:
   - Press `Ctrl+X`
   - Press `Y` to confirm
   - Press `Enter` to save

6. Restart the SSH service:
   ```
   sudo systemctl restart ssh
   ```

7. Exit the current session:
   ```
   exit
   ```

8. Log in as the new user:
   ```
   ssh newusername@<server-ip>
   ```

## 3. Install and Configure Redis

1. Update and upgrade your system:
   ```
   sudo apt update && sudo apt upgrade
   ```

2. Install Redis:
   ```
   sudo apt install redis-server
   ```

3. Start the Redis server:
   ```
   sudo service redis-server start
   ```

4. Verify Redis is running:
   ```
   redis-cli ping
   ```
   You should receive a "PONG" response.

### Redis Commands

To clear the entire Redis database:
```
redis-cli FLUSHALL
```

## 4. Python Environment Setup

1. Create and navigate to the project directory:
   ```
   mkdir fastapi && cd fastapi
   ```

2. Install Python virtual environment:
   ```
   sudo apt install python3.11-venv
   ```

3. Create a virtual environment:
   ```
   python3 -m venv env
   ```

4. Activate the virtual environment:
   ```
   source env/bin/activate
   ```

5. Create a requirements file:
   ```
   touch requirements.txt
   ```

6. Add the following content to `requirements.txt`:
   ```
   fastapi
   uvicorn
   redis
   slowapi
   pydantic-settings
   python-dotenv
   python-jose
   passlib
   python-multipart
   ```

7. Install the required packages:
   ```
   pip3 install -r requirements.txt
   ```

## 5. FastAPI Setup

(Assuming you have already set up your FastAPI application files)

## 6. Running the FastAPI Application

1. Ensure you're in the project directory with the virtual environment activated.
2. Start the application:
   ```
   python3 main.py
   ```
3. Your application will be accessible at `http://localhost:8000`.

## 7. Testing the Application

Use these curl commands to test your API:

1. Create a user: See [create-user.txt](commands/create-user.txt)
2. Login and get an access token: See [login-user.txt](commands/login-user.txt)
3. Test authenticated access: See [test-user.txt](commands/test-user.txt)

**Note**: Replace `<access_token>` in the test-user command with the actual token received from the login command.

## 8. Deployment

1. Install Nginx:
   ```
   sudo apt install nginx
   ```

2. Configure Nginx:
   ```
   sudo nano /etc/nginx/sites-available/default
   ```
   Replace the default config with the content from [default.txt](configs/default.txt)

3. Restart Nginx:
   ```
   sudo systemctl restart nginx
   ```

4. Install Supervisor:
   ```
   sudo apt install supervisor
   ```

5. Configure Supervisor:
   ```
   sudo nano /etc/supervisor/conf.d/fastapi.conf
   ```
   Replace the contents with [fastapi.conf](configs/fastapi.conf)
   - **Important**: Replace `user=tim` with the new user you created
   - **Important**: Replace `/path/venv/bin/uvicorn` with the path to your virtual environment
   - **Important**: Replace `/path/to/your/app` with the path to your application root dir

command=/path/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
directory=/path/to/your/app

6. Update Supervisor:
   ```
   sudo supervisorctl reread
   sudo supervisorctl update
   ```

7. Start your FastAPI application:
   ```
   sudo supervisorctl start fastapi
   ```

## 9. Test Your Public API

Your API should now be accessible via the public IP address of your Linode/Akamai instance.

To test, replace `<your-server-ip>` with your actual server IP in the curl commands from step 7.
