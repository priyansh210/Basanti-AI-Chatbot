import sentence_breakdown as sb
import new_features.wrapperfunctions as wf #has the functions calling apis. Change baseURL in backendrequests to connect to correct database
import new_features.bsnti as bsnti #has the classes

break_query = sb.break_querry

P = bsnti.People()
M = bsnti.Messages()
T = bsnti.Tasks()
S = bsnti.Schedules()
I = bsnti.Inventory()

while True:
    prompt = "Tell Ashwin to meet Herschelle tomorrow" #add funtion here to get input

    broken_query = break_query(prompt)

    match broken_query['FUNCTION']:
        case "ADD MESSAGE":
            necessary_params = ["WHO", "WHAT"] #add where to prompt if message has to be sent
            wf.checkNecessaryParams(broken_query, necessary_params)
            wf.createMessage(M, broken_query)
        case "SEND MESSAGE":
            necessary_params = ["WHO", "WHAT"] #add where to prompt if message has to be sent
            wf.checkNecessaryParams(broken_query, necessary_params)
            wf.createMessage(M, broken_query)
        case _:
            #apologize and prompt again for the query
            pass
    break

