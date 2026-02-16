"""gateway.__main__ — Start the gateway with uvicorn."""
import uvicorn

def main() -> None:
    uvicorn.run("gateway.main:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()
