import os
import requests


def download_file(url, target_path):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(target_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)


def download_file_range(url, target_path, start, end):
    headers = {"Range": f"bytes={start}-{end}"}
    with requests.get(url, headers=headers, stream=True) as response:
        response.raise_for_status()
        with open(target_path, 'ab') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)


def main():
    presigned_url = input("Enter the URL from email: ")
    all_models_list = [
        "meta-llama-3.1-405b",
        "meta-llama-3.1-70b",
        "meta-llama-3.1-8b",
        "meta-llama-guard-3-8b",
        "prompt-guard"
    ]

    print("\n **** Model list ***")
    for model in all_models_list:
        print(f" - {model}")

    selected_model = input("Choose the model to download: ")
    print(f"\n Selected model: {selected_model} \n")

    model_lists = {
        "meta-llama-3.1-405b": "meta-llama-3.1-405b-instruct-mp16,meta-llama-3.1-405b-instruct-mp8,meta-llama-3.1-405b-instruct-fp8,meta-llama-3.1-405b-mp16,meta-llama-3.1-405b-mp8,meta-llama-3.1-405b-fp8",
        "meta-llama-3.1-70b": "meta-llama-3.1-70b-instruct,meta-llama-3.1-70b",
        "meta-llama-3.1-8b": "meta-llama-3.1-8b-instruct,meta-llama-3.1-8b",
        "meta-llama-guard-3-8b": "meta-llama-guard-3-8b-int8-hf,meta-llama-guard-3-8b",
        "prompt-guard": ""
    }

    selected_models = ""
    model_list = model_lists.get(selected_model, "")

    if not model_list and selected_model != "prompt-guard":
        print("\n **** Available models to download: ***")
        for model in model_list.split(','):
            print(f" - {model}")
        selected_models = input("Enter the list of models to download without spaces or press Enter for all: ")

    target_folder = "."  # where all files should end up
    os.makedirs(target_folder, exist_ok=True)

    if not selected_models:
        selected_models = model_list

    print("Downloading LICENSE and Acceptable Usage Policy")
    download_file(presigned_url.replace('*', 'LICENSE'), os.path.join(target_folder, "LICENSE"))
    download_file(presigned_url.replace('*', 'USE_POLICY.md'), os.path.join(target_folder, "USE_POLICY.md"))

    for model in selected_models.split(','):
        additional_files = ""
        tokenizer_model = True
        pth_file_chunk_count = 0
        pth_file_count = 0
        model_path = ""

        if model == "meta-llama-3.1-405b-instruct-mp16":
            pth_file_count = 15
            pth_file_chunk_count = 2
            model_path = "Meta-Llama-3.1-405B-Instruct-MP16"
        elif model == "meta-llama-3.1-405b-instruct-mp8":
            pth_file_count = 7
            pth_file_chunk_count = 4
            model_path = "Meta-Llama-3.1-405B-Instruct-MP8"
        elif model == "meta-llama-3.1-405b-instruct-fp8":
            pth_file_count = 7
            pth_file_chunk_count = 3
            model_path = "Meta-Llama-3.1-405B-Instruct"
            additional_files = "fp8_scales_0.pt,fp8_scales_1.pt,fp8_scales_2.pt,fp8_scales_3.pt,fp8_scales_4.pt,fp8_scales_5.pt,fp8_scales_6.pt,fp8_scales_7.pt"
        elif model == "meta-llama-3.1-405b-mp16":
            pth_file_count = 15
            pth_file_chunk_count = 2
            model_path = "Meta-Llama-3.1-405B-MP16"
        elif model == "meta-llama-3.1-405b-mp8":
            pth_file_count = 7
            pth_file_chunk_count = 4
            model_path = "Meta-Llama-3.1-405B-MP8"
        elif model == "meta-llama-3.1-405b-fp8":
            pth_file_count = 7
            pth_file_chunk_count = 3
            model_path = "Meta-Llama-3.1-405B"
        elif model == "meta-llama-3.1-70b-instruct":
            pth_file_count = 7
            model_path = "Meta-Llama-3.1-70B-Instruct"
        elif model == "meta-llama-3.1-70b":
            pth_file_count = 7
            model_path = "Meta-Llama-3.1-70B"
        elif model == "meta-llama-3.1-8b-instruct":
            model_path = "Meta-Llama-3.1-8B-Instruct"
        elif model == "meta-llama-3.1-8b":
            model_path = "Meta-Llama-3.1-8B"
        elif model == "meta-llama-guard-3-8b-int8-hf":
            pth_file_count = -1
            model_path = "Meta-Llama-Guard-3-8B-INT8-HF"
            additional_files = "generation_config.json,model-00001-of-00002.safetensors,model-00002-of-00002.safetensors,model.safetensors.index.json,special_tokens_map.json,tokenizer_config.json,tokenizer.json"
            tokenizer_model = False
        elif model == "meta-llama-guard-3-8b":
            model_path = "Meta-Llama-Guard-3-8B"
        elif model == "prompt-guard":
            pth_file_count = -1
            model_path = "Prompt-Guard"
            additional_files = "model.safetensors,special_tokens_map.json,tokenizer_config.json,tokenizer.json"
            tokenizer_model = False

        print(f"\n***Downloading {model_path}***")
        os.makedirs(os.path.join(target_folder, model_path), exist_ok=True)

        if tokenizer_model:
            print("Downloading tokenizer")
            download_file(presigned_url.replace('*', f"{model_path}/tokenizer.model"), os.path.join(target_folder, model_path, "tokenizer.model"))

        if pth_file_count >= 0:
            for i in range(pth_file_count + 1):
                s = f"{i:02}"
                print(f"Downloading consolidated.{s}.pth")
                if pth_file_chunk_count > 0:
                    start = 0
                    chunk_size = 27000000001
                    for chunk_count in range(1, pth_file_chunk_count + 1):
                        end = start + chunk_size - 1
                        part_path = os.path.join(target_folder, model_path, f"part.{chunk_count}.pth")
                        download_file_range(presigned_url.replace('*', f"{model_path}/consolidated.{s}.pth"), part_path, start, end)
                        with open(os.path.join(target_folder, model_path, f"consolidated.{s}.pth"), 'ab') as consolidated:
                            with open(part_path, 'rb') as part:
                                consolidated.write(part.read())
                        os.remove(part_path)
                        start = end + 1
                else:
                    download_file(presigned_url.replace('*', f"{model_path}/consolidated.{s}.pth"), os.path.join(target_folder, model_path, f"consolidated.{s}.pth"))

        for additional_file in additional_files.split(','):
            print(f"Downloading {additional_file}...")
            download_file(presigned_url.replace('*', f"{model_path}/{additional_file}"), os.path.join(target_folder, model_path, additional_file))

        if model not in ["prompt-guard", "meta-llama-guard-3-8b-int8-hf"]:
            print("Downloading params.json...")
            download_file(presigned_url.replace('*', f"{model_path}/params.json"), os.path.join(target_folder, model_path, "params.json"))

if __name__ == "__main__":
    main()
