module.exports = {
  apps: [
    {
      name: "botbako",
      script: "./main.py",
      interpreter: "./venv/Scripts/python.exe", // Sesuaikan dengan folder virtual environment-mu jika berbeda (misal .venv)
      watch: false,
      autorestart: true,
      max_memory_restart: "250M", // Restart bot jika memori melebihi 250MB (mencegah memory leak)
      env: {
        NODE_ENV: "production",
        PYTHONPATH: ".",
      },
      log_date_format: "YYYY-MM-DD HH:mm Z",
      error_file: "./logs/pm2-error.log",
      out_file: "./logs/pm2-out.log",
    },
  ],
};
