# Elements

_This module contains the classes representing the elements of the diagram._

## Element base class

The `Element` class is the base class for all elements in the diagram. It has the following attributes:

- `element_type`: an enum containing the type of the element (e.g. `Interface`, `Message`, `State`, `ChoicePoint`, or `Transition`).
- `identifier`: an integer containing the identifier of the element.

## Interface

The `Interface` class is a subclass of `Element` with the type set to `Interface` and is responsible for holding the data of an interface. It has the following additional attributes:

- `name`: a string containing the name of the interface.

## Message

The `Message` class is a subclass of `Element` with the type set to `Message` and is responsible for holding the data of a message. It has the following additional attributes:

- `name`: a string containing the name of the message.
- `interface`: a string containing the name of the interface of the message.

## State

The `State` class is a subclass of `Element` with the type set to `State` and is responsible for holding the data of a state. It has the following additional attributes:

- `name`: a string containing the name of the state.
- `display_name`: a string containing the display name of the state.

## Choice-point

The `ChoicePoint` class is a subclass of `Element` with the type set to `ChoicePoint` and is responsible for holding the data of a choice-point. It has the following additional attributes:

- `name`: a string containing the name of the choice-point.
- `question`: a string containing the question of the choice-point.

## Transition

The `Transition` class is a subclass of `Element` with the type set to `Transition` and is responsible for holding the data of a transition. It has the following additional attributes:

- `source_state`: a `State` object containing the source state of the transition.
- `target_state`: a `State` object containing the target state of the transition.
- `connector_type`: an enum (`Left`, `Right`, `Up`, `Down`) containing the type of the connector of the transition.
- `connector_length`: an integer containing the length of the connector of the transition.
- `messages`: a list of `Message` objects containing the messages of the transition.
