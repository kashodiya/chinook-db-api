







import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=56313,  # Using the alternative port provided in the runtime information
        reload=True,
        log_level="info"
    )







