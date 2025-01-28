from backend.gpt_utils.gpt_client import GptClient

if __name__ == "__main__":
    print("Running test")
    session = GptClient()
    result = session._produce_completion("I am testing your API. Respond with the user prompt but propperly capitalized", "i am the mayor. i am tired")
    print(result)

    result = session._choose_option("Select the option that is not a real language:",  ["japanese", "spanish", "english", "postinese", "portuguese"])
    print(result)

    result = session._choose_subset("Select the options that you generally deem as good practices in python", 
                                    [
                                        "Commenting your code",
                                        "Naming variables a single letter",
                                        "Writing all your code in a single huge file",
                                        "Using desing patterns to make your OOP code reusable and modular"
                                    ])
    print(result)

    result = session._produce_list("Produce a list of at least 3 states in the USA")
    print(result)
    

