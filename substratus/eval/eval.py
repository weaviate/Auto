import json
import argparse
import re
import weaviate
from weaviate.embedded import EmbeddedOptions



def loadDataFromJSON(filepath):
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data


def json_reader(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as api_ref_fh:
        data = json.load(api_ref_fh)
    return data


def didItExecute(WeaviateClient, schemaPath, modelOutput):
    WeaviateClient.schema.delete_all()
    schema = json_reader(f'../../dataEngine/data/ToySchemas/{schemaPath}')
    WeaviateClient.schema.create(schema)
    WeaviateResponse = client.query.raw(modelOutput)
    return WeaviateResponse
    # check keys of Weaviate Response

def GPTEval(instruction, response):
    prompt = """
    %s, %s
    """ % (instruction, response)
    return 0
    # put openai request in here

def extract_graphql_code(text):
    pattern = r'```graphql(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)[0]
    return matches

def main():
    parser = argparse.ArgumentParser(description="Weaviate Gorilla LLM evaluator")
    parser.add_argument("-f", "--file", type=str, required=True, help="Path to test dataset with responses")
    args = parser.parse_args()


    # Load Data
    responses = loadDataFromJSON(args.file)
    # Connect to Weaviate
    client = weaviate.Client(
      embedded_options=EmbeddedOptions()
    )

    counter = 1
    successfulQueries = []
    failedQueries = []
    failedAPIsCount = {}
    failedSchemasCount = {}
    for idx, example in enumerate(responses):

        failed = False
        try:
            modelQuery = extract_graphql_code(example["modelOutput"])
        except:
            failed = True

        weaviateResponse = didItExecute(client, example["schemaPath"], modelQuery)

        if "errors" in weaviateResponse.keys():
            failed = True

        if failed:
            print("FAILED! FAILED! FAILED! \n")
            print(idx)
            failedQueries.append(example)
            # Update failed Schema tracker
            if example["schemaPath"] in failedSchemasCount.keys():
                failedSchemasCount[example["schemaPath"]] += 1
            else:
                failedSchemasCount[example["schemaPath"]] = 1
            # Update API tracker
            if example["apiRefPath"] in failedAPIsCount.keys():
                failedAPIsCount[example["apiRefPath"]] += 1
            else:
                failedAPIsCount[example["apiRefPath"]] = 1
        else:
            successfulQueries.append(example)

    print(f"{len(successfulQueries)} Queries successfully executed!")
    print(f"{len(failedQueries)} Queries failed to execute!")
    print("FAILED API Count \n")
    print(failedAPIsCount)
    print("FAILE SCHEMA COUNT \n")
    print(failedSchemasCount)

if __name__ == "__main__":
    main()