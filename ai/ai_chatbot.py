import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
import os
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def get_ai_response(user_input, tax_calculator):
    """Get a response from the AI chatbot, handling tool calls if necessary"""
    try:
        messages = [
            {"role": "system", "content": "You are a helpful tax assistant."},
            {"role": "user", "content": user_input}
        ]
        
        # Initial API call with tool definition
        chat_completion = client.chat.completions.create(
            messages=messages,
            tools=[{
                "type": "function",
                "function": {
                    "name": "process_tax_return",
                    "description": "Process a complete tax return comparing both tax regimes and recommending the better option",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "gross_income": {
                                "type": "number",
                                "description": "The total annual gross income in INR"
                            },
                            "regime": {
                                "type": "string",
                                "description": "Which regime to calculate: 'new', 'old', or 'both'",
                                "enum": ["new", "old", "both"],
                                "default": "both"
                            },
                            "has_house_loan": {
                                "type": "boolean",
                                "description": "Whether the individual has a housing loan",
                                "default": False
                            },
                            "has_elss": {
                                "type": "boolean",
                                "description": "Whether the individual has ELSS investments",
                                "default": False
                            },
                            "has_health_insurance": {
                                "type": "boolean",
                                "description": "Whether the individual has health insurance",
                                "default": False
                            },
                            "has_nps": {
                                "type": "boolean",
                                "description": "Whether the individual has NPS contributions",
                                "default": False
                            },
                            "section_80c_amount": {
                                "type": "number",
                                "description": "Amount invested under Section 80C (max ₹1,50,000)",
                                "default": 0
                            },
                            "health_insurance_premium": {
                                "type": "number",
                                "description": "Health insurance premium paid (max ₹25,000)",
                                "default": 0
                            },
                            "nps_contribution": {
                                "type": "number",
                                "description": "NPS contribution amount (max ₹50,000)",
                                "default": 0
                            },
                            "housing_loan_interest": {
                                "type": "number",
                                "description": "Interest paid on housing loan (max ₹2,00,000)",
                                "default": 0
                            },
                            "hra_received": {
                                "type": "number",
                                "description": "HRA received from employer",
                                "default": 0
                            },
                            "hra_rent_paid": {
                                "type": "number",
                                "description": "Actual rent paid",
                                "default": 0
                            },
                            "is_metro": {
                                "type": "boolean",
                                "description": "Whether the individual lives in a metro city for HRA calculation",
                                "default": False
                            }
                        },
                        "required": ["gross_income"]
                    }
                }
            }],
            model="llama-3.3-70b-versatile"
        )
        
        response_message = chat_completion.choices[0].message
        
        # Check if the AI wants to use tools
        if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
            messages.append(response_message)  # Append initial response with tool calls
            for tool_call in response_message.tool_calls:
                if tool_call.function.name == "process_tax_return":
                    function_args = json.loads(tool_call.function.arguments)
                    try:
                        # Execute the tool using tax_calculator instance
                        function_response = tax_calculator.process_tax_return(**function_args)
                        # Convert result to JSON string for AI
                        function_response_str = json.dumps(function_response)
                    except Exception as e:
                        function_response_str = f"Tool error: {str(e)}"
                    
                    # Append tool result to messages
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": "process_tax_return",
                            "content": function_response_str,
                        }
                    )
            print(messages)
            # Second API call with tool results
            second_response = client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile"
            )
            print(second_response.choices[0].message.content)
            return second_response.choices[0].message.content
        else:
            # No tool calls; return direct response
            
            return response_message.content

    except Exception as e:
        return f"Error: {str(e)}"