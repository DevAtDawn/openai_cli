import os
import openai
import sys
import getpass

# export OPENAI_API_KEY='xxx'

def read_config_file():
    # read from config file
    config_file = os.path.join(os.path.expanduser("~"), ".openai_cli")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            oaikey = f.read()
            return oaikey
    else:
    # if dir aqnd file does not exist create it
        if not os.path.exists(os.path.dirname(config_file)):
            try:
                os.makedirs(os.path.dirname(config_file))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        # create file
        with open(config_file, "w") as f:
            f.write("")
        return None

def save_config_file(oaikey):
    config_file = os.path.join(os.path.expanduser("~"), ".openai_cli")
    with open(config_file, "w") as f:
        f.write(oaikey)

def openai_api(**kwargs):

    # if 'api_key' in kwargs and 'api_key' is not None:
    #     openai.api_key = kwargs.get('api_key')
    # else:
    #     openai.api_key = os.getenv("OPENAI_API_KEY")
    oaikey = kwargs.get("api_key")

    # if oaikey is empty or None
    if not oaikey:
        oaikey = os.getenv("OPENAI_API_KEY")

    # if oaikey is empty or None
    if not oaikey:
        # read from config file
        oaikey = read_config_file()
    # if oaikey is empty or None after reading from config file read from user input
    if not oaikey:
        # pass
        # oaikey = input("Enter OpenAI API Key: ")
        oaikey = getpass.getpass("Enter OpenAI API Key: ")
        # save to config file
        save_config_file(oaikey)

    openai.api_key = oaikey

    model = kwargs["model"]

    if model == "code-davinci-edit-001" or model == "text-davinci-edit-001":
        # Note: can put if prompt is None check here, then use args[1]
        response = openai.Edit.create(
            model=kwargs["model"],
            input=kwargs["prompt"],
            instruction=kwargs["instruction"],
            temperature=kwargs["temperature"],
            top_p=kwargs["top_p"],
        )

    if model == "code-davinci-002" or model == "code-davinci-001":
        response = openai.Completion.create(
            model=kwargs["model"],
            prompt=kwargs["prompt"],
            temperature=kwargs["temperature"],
            max_tokens=kwargs["max_tokens"],
            top_p=kwargs["top_p"],
            frequency_penalty=kwargs["frequency_penalty"],
            presence_penalty=kwargs["presence_penalty"],
            stop=kwargs["stop"],
        )

    # print(response)
    output = response.choices[0].text
    return output


def get_args():

    default_dict = {}

    if not sys.stdin.isatty():
        stdin = sys.stdin.read()
        default_dict["stdin"] = stdin
    else:
        stdin = None
        default_dict["stdin"] = None

    args = sys.argv


    # if -m arg is passed, set the model to the value of the arg
    if "-m" in args or "--model" in args:
        model = args[args.index("-m") + 1]
        default_dict["model"] = model

    else:
        model = None
        # model = "code-davinci-edit-001"
        default_dict["model"] = model

    if model is None:
        model = "code-davinci-edit-001"
        default_dict = {
            "model": "code-davinci-edit-001",
            "prompt": None,
            "instruction": None,
            "temperature": 0,
            "top_p": 1,
        }
        default_dict["model"] = model
        if default_dict["prompt"] is None:
            prompt = args[1]
            default_dict["prompt"] = args[1]
        if default_dict["instruction"] is None:
            # if theres 2 args, set instruction to the 2nd arg
            # print(len(args))
            if len(args) == 3:
                instruction = args[2]
                default_dict["instruction"] = args[2]
            #elif only 1 arg passed and stdin is not empty, set instruction to arg1
            elif len(args) == 2 and stdin is not None:
                instruction = args[1]
                default_dict["instruction"] = args[1]
            else:
                instruction = args[2]
                default_dict["instruction"] = instruction

    elif model == "code-davinci-edit-001":
        default_dict = {
            "model": "code-davinci-edit-001",
            "prompt": None,
            "instruction": None,
            "temperature": 0,
            "top_p": 1,
        }

    elif model == "text-davinci-edit-001":
        default_dict = {
            "model": None,
            "prompt": None,
            "instruction": None,
            "temperature": 0.7,
            "top_p": 1,
        }
        default_dict["model"] = model

    elif model == "code-davinci-001" or model == "code-davinci-002":
        default_dict = {
            "model": None,
            "prompt": None,
            "temperature": 0,
            "max_tokens": 182,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            # "stop": ["###"],
            "stop": None,
        }
        default_dict["model"] = model

    # if -i arg is passed, set the instruction to the value of the arg
    if "-i" in args or "--instruction" in args:
        instruction = args[args.index("-i") + 1]
        default_dict["instruction"] = instruction
    elif len(args) == 3:
        instruction = args[2]
        default_dict["instruction"] = args[2]
    #elif only 1 arg passed and stdin is not empty, set instruction to arg1
    elif len(args) == 2 and stdin is not None:
        instruction = args[1]
        default_dict["instruction"] = args[1]
    else:  # and model == "code-davinci-edit-001": or model == "text-davinci-edit-001":
        instruction = args[2]
        default_dict["instruction"] = instruction

    # if -p arg is passed, set the prompt to the value of the arg
    if "-p" in args or "--prompt" in args or "--input" in args:
        prompt = args[args.index("-p") + 1]
        default_dict["prompt"] = prompt
    elif "-f" in args or "--file" in args:
        file_path = args[args.index("-f") + 1]
        with open(file_path, "r") as f:
            prompt = f.read()
        default_dict["prompt"] = prompt
    elif stdin is not None:
        prompt = stdin
        default_dict["prompt"] = prompt
        # if only on 1 arg pass and stdin is not None, set prompt to stdin, set instruction to arg1, also allow passing of args without ""
        if len(args) == 2:
            instruction = args[1]
            default_dict["instruction"] = instruction
    else:
        prompt = args[1]
        default_dict["prompt"] = prompt

    # if --temperature arg ispassed, set the temperature to the value of the arg
    if "--temperature" in args:
        temperature = args[args.index("--temperature") + 1]
        default_dict["temperature"] = int(temperature)

    # if --max_tokens arg is passed, set the max_tokens to the value of the arg
    if "--max_tokens" in args:
        max_tokens = args[args.index("--max_tokens") + 1]
        default_dict["max_tokens"] = int(max_tokens)

    # if --top_p arg is passed, set the top_p to the value of the arg
    if "--top_p" in args:
        top_p = args[args.index("--top_p") + 1]
        default_dict["top_p"] = top_p

    # if --frequency_penalty arg is passed, set the frequency_penalty to the value of the arg
    if "--frequency_penalty" in args:
        frequency_penalty = args[args.index("--frequency_penalty") + 1]
        default_dict["frequency_penalty"] = int(frequency_penalty)

    # if --presence_penalty arg is passed, set the presence_penalty to the value of the arg
    if "--presence_penalty" in args:
        presence_penalty = args[args.index("--presence_penalty") + 1]
        default_dict["presence_penalty"] = int(presence_penalty)

    # if --pipe arg is passed, set the stdin to the value of the arg
    if "--pipe" in args:
        # pipe = args[args.index("--pipe") + 1]
        # default_dict["pipe"] = pipe
        lastline = stdin.splitlines()
        lastline = [x for x in lastline if x]
        lastline = lastline[-1]
        instruction = lastline
        default_dict["instruction"] = lastline
        prompt = stdin.rsplit(lastline, 1)[0]
        default_dict["prompt"] = prompt
       
    # if --fpi arg is passed, set the stdin to the value of the arg
    if "-fpi" in args or "--fpi" in args:
        file_path = args[args.index("-fpi") + 1]
        with open(file_path, "r") as f:
            data = f.read()
            lastline = data.splitlines()
            lastline = [x for x in lastline if x]
            lastline = lastline[-1]
            instruction = lastline
            default_dict["instruction"] = lastline
            prompt = data.rsplit(lastline, 1)[0]
            default_dict["prompt"] = prompt

    if "--stop" in args:
        stop = args[args.index("--stop") + 1]
        default_dict["stop"] = stop
        
    return default_dict

def cli():
    default_dict = get_args()
    output = openai_api(**default_dict)
    print(output)
#     return output
#     print(output, default_dict)


if __name__ == "__main__":
    cli()
 
