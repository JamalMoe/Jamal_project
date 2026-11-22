from Jamal_project.config import load_config

config = load_config()

threads = config["scanner"]["default_threads"]
timeout = config["scanner"]["timeout"]

print(threads)
print(timeout)