# Paper summarizer

* Copy from [Lucas Soares @ medium](https://medium.com/geekculture/summarize-papers-with-chatgpt-8737ed520a07)

## How to use

1. Install required packages

    ```bash
    poetry update
    ```

2. Update the openai api key in the .env file
    * If you are admin user, just decrypt the file with blackbox by the following command

        ```bash
        blackbox_decrypt_all_files
        ```

    * For non-admin user, please create a .env file following the .env.example

3. Try the code with the following command

    ```bash
    poetry run python main.py
    ```
