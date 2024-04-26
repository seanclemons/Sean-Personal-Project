import json

room_options = ['HSL', 'UGL']
study_room_lengths = ['30 minutes', '1 hour']

def validate_order(slots):
    # Validate RoomOption
    if not slots['RoomOption']:
        print('Validating RoomOption Slot')
        return {
            'isValid': False,
            'invalidSlot': 'RoomOption'
        }

    if slots['RoomOption']['value']['originalValue'].upper() not in room_options:
        print('Invalid RoomOption')
        return {
            'isValid': False,
            'invalidSlot': 'RoomOption',
            'message': 'Please select either HSL or UGL for the room option.'
        }

    # Validate StudyRoomLength
    if not slots['StudyRoomLength']:
        print('Validating StudyRoomLength Slot')
        return {
            'isValid': False,
            'invalidSlot': 'StudyRoomLength'
        }

    if slots['StudyRoomLength']['value']['originalValue'] not in study_room_lengths:
        print('Invalid StudyRoomLength')
        return {
            'isValid': False,
            'invalidSlot': 'StudyRoomLength',
            'message': 'Please select either 30 minutes or 1 hour for the study room length.'
        }

    # Valid Order
    return {'isValid': True}


def lambda_handler(event, context):
    print(event)

    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    order_validation_result = validate_order(slots)

    if event['invocationSource'] == 'DialogCodeHook':
        if not order_validation_result['isValid']:
            if 'message' in order_validation_result:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": order_validation_result['message']
                        }
                    ]
                }
            else:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    }
                }
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }

    if event['invocationSource'] == 'FulfillmentCodeHook':
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "slots": slots,
                    "state": "Fulfilled"
                }

            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Your study room order has been placed."
                }
            ]
        }

    print(response)
    return response
