# movie_suggestor

## Description

This is a simple movie suggestor that uses the tmdb database to suggest movies based on the user's input. The user can input a movie title and the program will return a list of movies that are similar to the input movie. The program uses a cosine similarity algorithm to determine the similarity between movies.
The frontend is built using React and the backend is built using FastAPI.

![movie_suggestor](https://cloud-2wqfvyztt-hack-club-bot.vercel.app/0image.png)

## How to use

Run the `run.sh` file to start the program.
The script will start both the frontend and backend servers.

```bash
./run.sh
```

The frontend will be available at `http://localhost:8010` and the backend will be available at `http://localhost:8011`.

## Requirements

- Python 3.8

### Python packages

1. create a virtual environment

    ```bash
    python3 -m venv venv
    ```

2. Activate the virtual environment

    ```bash
    source venv/bin/activate
    ```

3. Install the required packages

    ```bash
    pip install -r requirements.txt
    ```

### Node packages

1. Install the required packages

    ```bash
    npm install
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

[Neetre](https://github.com/Neetre)