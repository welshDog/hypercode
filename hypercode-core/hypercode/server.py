from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from hypercode.compiler import compile_flow
from hypercode.simulator import simulate_flow

app = FastAPI(title="HyperCode Backend API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FlowRequest(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    viewport: Optional[Dict[str, Any]] = None

@app.get("/")
async def root():
    return {"message": "HyperCode Backend Online", "status": "ready"}

@app.post("/compile")
async def compile_endpoint(flow: FlowRequest):
    """
    Compiles a Visual Flow into HyperCode source text.
    """
    try:
        # Convert Pydantic model to dict
        flow_data = flow.model_dump()
        
        # Generate Code
        source_code = compile_flow(flow_data)
        
        # Run Simulation
        simulation_results = simulate_flow(flow_data)
        
        return {
            "success": True,
            "code": source_code,
            "simulation": simulation_results,
            "message": "Compilation and Simulation successful"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
