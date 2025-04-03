# COLA: COpilot for Landscape Architecture

## Introducing COLA

COLA, short for COpilot for Landscape Architecture, is a human-in-the-loop Landscape Achitecture design system based on agents. Its formalized definition is COLA(M,A,R,S), where M stands for Modeler(i.e. the agent who model the design plan), A stands for Adapter(i.e. the agent who adapt the plan into image prompt), R stands for Renderer(i.e. the agent who render the prototype image), S stands for Supervisor(i.e. the human designer) .

## Running COLA

**These instructions assume you are in the `COLA/` directory**

### Running the Agent

First, install the backend dependencies:

```sh
cd agent
poetry install
```

Then, create a `.env` file inside `./agent-py` or `./agent-js` with the following:

```
OPENAI_API_KEY=...
TAVILY_API_KEY=...
```

Then, run:

```sh
poetry run dev
```

### Running the UI

First, install the frontend dependencies:

```sh
cd ui
pnpm i
```

Then, create a `.env` file inside `./ui` with the following:

```
OPENAI_API_KEY=...
```

Then, run the Next.js project:

```sh
pnpm run dev
```

### Usage

Navigate to [http://localhost:3000](http://localhost:3000).

### Running the LangGraph Studio

Run the LangGraph studio:
```sh
cd agent
langgraph dev
```
