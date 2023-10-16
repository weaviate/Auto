# Eval notebook to evaluate Weaviate Gorilla LLM


## Testing locally
```
docker build -t eval .
```

```
docker run -it \
  -v $(pwd)/eval.ipynb:/content/eval.ipynb \
  -v $(pwd)/params.json:/content/params.json \
  -v $(pwd)/artifacts:/content/artifacts \
  -p 8888:8888 \
  eval serve-notebook.sh
```
