# Project
AI Travel Agent and Expense Planner

## Overview
An intelligent, real-time travel assistant and budgeting planner built using LangChain, LangGraph, and custom API-powered tools. The system generates comprehensive travel plans and expense estimates for any destination using weather, accommodation, currency, and attraction data.

## Features
### Natural Language Travel Planning
Input a prompt like "Plan a trip to Milan for 10 days with budget in USD", and the AI handles the rest.

### Tool-Enhanced Responses
Dynamically uses tools to gather real-time:
- Weather and forecasts
- Hotel/accommodation options
- Top attractions
- Currency conversion and budgeting

### Dynamic Graph Workflow
Uses LangGraph to route messages between LLM and tools in a conditional execution flow.

## Tools

| Tool Name         | Functionality                                                      |
|-------------------|--------------------------------------------------------------------|
| `Weather`         | Fetches real-time weather and forecasts via WeatherAPI             |
| `TopAttractions`  | Retrieves top-rated tourist places using Foursquare Places API     |
| `Accommodation`   | Searches for hotels with ratings, prices, and links via DuckDuckGo |
| `CurrencyExchange`| Converts currencies using Fixer API                                |


## Setup Instructions
1. Clone the repository
```bash
git clone https://github.com/your-username/ai-travel-planner.git
cd ai-travel-planner

```
2. Create and Populate .env
```env
OPENAI_API_KEY=your_openai_key
WEATHER_API_KEY=your_weatherapi_key
FOURSQUARE_API_KEY=your_foursquare_key
FOREX_API_KEY=your_fixer_key
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Future Improvements
- Add food planning tool
- Add flight search integration
- Extend budgeting to include daily activity expenses
- Multilingual support

## License
This project is licensed under the Raza Mehar License. See the LICENSE.md file for details.

## Contact
For any questions or clarifications, please contact Raza Mehar at [raza.mehar@gmail.com].