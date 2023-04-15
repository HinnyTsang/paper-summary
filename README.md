# Paper summarizer

Summarize papers with [ChatGPT API](https://chat.openai.com/)

* Copy from [Lucas Soares @ medium](https://medium.com/geekculture/summarize-papers-with-chatgpt-8737ed520a07)

## How to use

1. Install required packages

    ```bash
    poetry update
    ```

2. Update the Openai API key in the .env file
    * If you are an admin user, just decrypt the file with Blackbox by the following command

        ```bash
        make secrets
        ```

    * For non-admin users, please create a .env file following the .env.example

3. Try the code with the following command

    ```bash
    poetry run python main.py
    ```
