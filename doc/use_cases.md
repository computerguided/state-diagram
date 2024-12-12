# Use cases

_Given the [design of the GUI](./gui_design.md), this section describes the use cases of the application from the user's perspective._

## Overview

The application has the following use cases:

1. [Start the application](#use-case-1---start-the-application)
2. [Create a new diagram](#use-case-2-create-a-new-diagram)
3. [Open an existing diagram](#use-case-3-open-an-existing-diagram)
4. [Save the current diagram](#use-case-4-save-the-current-diagram)
5. [Add a new state](#use-case-5-add-a-new-state)
6. [Add a new choice-point](#use-case-6-add-a-new-choice-point)
7. [Add a new interface](#use-case-7-add-a-new-interface)
8. [Select an interface](#use-case-8-select-an-interface)
9. [Deselect the interface](#use-case-9-deselect-the-interface)
10. [Delete the selected interface](#use-case-10-delete-the-selected-interface)
11. [Add a new message](#use-case-11-add-a-new-message)
12. [Select a message](#use-case-12-select-a-message)
13. [Deselect the message](#use-case-13-deselect-the-message)
14. [Delete the selected message](#use-case-14-delete-the-selected-message)
15. [Add a new transition](#use-case-15-add-a-new-transition)
16. [Select an element in the diagram canvas](#use-case-16-select-an-element-in-the-diagram-canvas)
17. [Deselect an element in the diagram canvas](#use-case-17-deselect-an-element-in-the-diagram-canvas)
18. [Edit the properties of a selected diagram element](#use-case-18-edit-the-properties-of-a-selected-diagram-element)
19. [Delete the selected diagram elements](#use-case-19-delete-the-selected-diagram-elements)

These use cases are described in more detail below.

## Use case 1 - Start the application

**Objective**: Start the application to start editing diagrams.

### Scenario 1.1 - Normal flow

**Preconditions**: The application is not running.

**Steps**:

1. The user starts the application.
2. The main window is created and displayed.
3. The default state diagram is created and shown in the diagram canvas.

## Use case 2: Create a new diagram

**Objective**: Create a new diagram.

### Scenario 2.1 - Indicate creation of a new diagram

**Preconditions**: The user wants to create a new diagram.

**Steps**:

1. The user selects "File" -> "New" in the menu bar.
2. It is checked if there are no unsaved edits in the current diagram.

**Continuation**: If there are unsaved edits in the current diagram, continue with [Scenario 2.3](#scenario-23---unsaved-edits-in-the-current-diagram), otherwise continue with [Scenario 2.2](#scenario-22---load-default-state-diagram).

### Scenario 2.2 - Load default state diagram

**Preconditions**: The current diagram can be deleted ([Scenario 2.2](#scenario-22---no-unsaved-edits-in-the-current-diagram) or [Scenario 2.5](#scenario-25---deletion-of-the-current-diagram)).

**Steps**:

1. The current diagram is deleted and the diagram canvas is cleared.
2. The default state diagram is created and loaded.

**Postconditions**: The default state diagram is shown in the diagram canvas.

### Scenario 2.3 - Unsaved edits in the current diagram

**Preconditions**: [Scenario 2.1](#scenario-21---indicate-creation-of-a-new-diagram) is completed and there are unsaved edits in the current diagram.

**Steps**:

1. A dialog is shown to the user asking to confirm the deletion of the current diagram.

**Continuation**: If the user wants to keep the edits in the current diagram, continue with [Scenario 2.4](#scenario-24---cancel-the-deletion-of-the-current-diagram), otherwise continue with [Scenario 2.5](#scenario-25---deletion-of-the-current-diagram).

### Scenario 2.4 - Cancel the deletion of the current diagram

**Preconditions**: [Scenario 2.3](#scenario-23---unsaved-edits-in-the-current-diagram) is completed and the user wants to keep the edits in the current diagram.

**Steps**:

1. The user cancels the deletion of the current diagram.
2. The dialog is closed.

**Postconditions**: The current diagram is not deleted and the diagram canvas is not cleared.

### Scenario 2.5 - Deletion of the current diagram

**Preconditions**: [Scenario 2.3](#scenario-23---unsaved-edits-in-the-current-diagram) is completed and the user does not want to keep the edits in the current diagram.
**Steps**:

1. The user confirms the deletion of the current diagram.
2. The dialog is closed.

**Continuation**: [Scenario 2.2](#scenario-22---load-default-state-diagram)

## Use case 3: Open an existing diagram

**Objective**: Load an existing diagram.

### Scenario 3.1 - Indicate opening of an existing diagram

**Preconditions**: The user wants to open an existing diagram.

**Steps**:

1. The user selects "File" -> "Open" in the menu bar.
2. It is checked if the current diagram is edited and if the edits are saved.

**Continuation**: If the current diagram is edited and the edits are not saved, continue with [Scenario 3.4](#scenario-34---unsaved-edits-in-the-current-diagram), otherwise continue with [Scenario 3.2](#scenario-32---select-diagram-file).

### Scenario 3.2 - Select diagram file

**Preconditions**: The current diagram can be deleted ([Scenario 3.1](#scenario-31---indicate-opening-of-an-existing-diagram) or [Scenario 3.6](#scenario-36---deletion-of-the-current-diagram)).

**Steps**:

1. A file dialog is opened in which the user can select a diagram file or cancel the opening of a diagram.

**Continuation**: If the user cancels the opening of a diagram, continue with [Scenario 3.9](#scenario-39---cancel-the-opening-of-a-diagram), otherwise continue with [Scenario 3.3](#scenario-33---select-diagram-file).

### Scenario 3.3 - Select diagram file

**Preconditions**: [Scenario 3.2](#scenario-32---select-diagram-file) is completed.

**Steps**:

1. The user selects a diagram file from the file dialog.
2. The user presses the "Open" button.
3. The selected diagram is loaded and the validity of the diagram is checked.

**Continuation**: If the diagram is valid, continue with [Scenario 3.7](#scenario-37---opening-a-correct-diagram), otherwise continue with [Scenario 3.8](#scenario-38---opening-a-faulty-diagram).

### Scenario 3.4 - Unsaved edits in the current diagram

**Preconditions**: [Scenario 3.1](#scenario-31---indicate-opening-of-an-existing-diagram) is completed and the current diagram is edited but not saved.

**Steps**:

1. A dialog is shown to the user asking to confirm the deletion of the current diagram.

**Continuation**: If the user wants to keep the edits in the current diagram, continue with [Scenario 3.5](#scenario-35---cancel-the-deletion-of-the-current-diagram), otherwise continue with [Scenario 3.6](#scenario-36---deletion-of-the-current-diagram).

### Scenario 3.5 - Cancel the deletion of the current diagram

**Preconditions**: [Scenario 3.4](#scenario-34---unsaved-edits-in-the-current-diagram) is completed and the user wants to keep the edits in the current diagram.

**Steps**:

1. The user cancels the deletion of the current diagram.
2. The dialog is closed.

**Postconditions**: The current diagram is not deleted and the diagram canvas is not cleared.

### Scenario 3.6 - Deletion of the current diagram

**Preconditions**: [Scenario 3.4](#scenario-34---unsaved-edits-in-the-current-diagram) is completed and the user wants to delete the edits in the current diagram.

**Steps**:

1. The user confirms the deletion of the current diagram.
2. The dialog is closed.

**Continuation**: [Scenario 3.2](#scenario-32---select-diagram-file)

### Scenario 3.7 - Opening a correct diagram

**Preconditions**: [Scenario 3.3](#scenario-33---select-diagram-file) is completed and the user selected a valid diagram.

**Steps**:

1. The current diagram is deleted and the diagram canvas is cleared.
2. The selected diagram is loaded.

**Postconditions**: The loaded diagram is shown in the diagram canvas.

### Scenario 3.8 - Opening a faulty diagram

**Preconditions**: [Scenario 3.3](#scenario-33---select-diagram-file) is completed and the user selected a faulty diagram.

**Steps**:

1. An error message is shown indicating that the selected diagram is faulty.
2. The user presses the "OK" button in the error message dialog.
3. The dialog is closed.

**Postconditions**: The current diagram is not deleted and the diagram canvas is not cleared.

### Scenario 3.9 - Cancel the opening of a diagram

**Preconditions**: [Scenario 3.1](#scenario-31---indicate-opening-of-an-existing-diagram) is completed and the user wants to cancel the opening of a diagram.

**Steps**:

1. The user cancels the opening of a diagram.
2. The dialog is closed.

**Postconditions**: The current diagram is not deleted and the diagram canvas is not cleared.

## Use case 4: Save the current diagram

**Objective**: Save the current diagram.

### Scenario 4.1 - First save

**Preconditions**: The user wants to save the current diagram for the first time.

**Steps**:

1. The user selects "File" -> "Save" in the menu bar.
2. A file dialog is opened to the user to select a file name.
3. The user selects a file name from the file dialog.
4. The current diagram is saved.

### Scenario 4.2 - Save the current diagram

**Preconditions**: The user wants to save the current diagram which was already saved before.

**Steps**:

1. The user selects "File" -> "Save" in the menu bar.
2. The current diagram is saved.

### Scenario 4.3 - Cancel the saving of the current diagram

**Preconditions**: The user wants to cancel the saving of the current diagram.

**Steps**:

1. The user cancels the saving of the current diagram.
2. The dialog is closed.
3. The current diagram is not saved.

### Scenario 4.4 - Save the current diagram as a new file

**Preconditions**: The user wants to save the current diagram as a new file.

**Steps**:

1. The user selects "File" -> "Save As" in the menu bar.
2. A file dialog is opened to the user to select a file name.
3. The user selects a file name from the file dialog.
4. The current diagram is saved.

## Use case 5: Add a new state

**Objective**: Add a new state to the current diagram.

### Scenario 5.1 - Open the state properties dialog

**Preconditions**: The user wants to add a new state to the current diagram.

**Steps**:

1. The user presses the "Add State" button in the toolbar.
2. The state properties dialog is shown.

### Scenario 5.2 - Add state with a unique name

**Preconditions**: [Scenario 5.1](#scenario-51---open-the-state-properties-dialog) is completed and the user wants to give the new state a unique name.

**Steps**:

1. The user fills in the unique state name.
4. Optionally, the user fills in display name.

### Scenario 5.3 - Save the new state

**Preconditions**: [Scenario 5.2](#scenario-52---add-state-with-a-unique-name) is completed and the user wants to save the new state.

**Steps**:

1. The user presses the "OK" button.
2. The state properties dialog is closed.
3. The new state is added to the diagram canvas and the states list.

### Scenario 5.4 - Try to add state with an existing name

**Preconditions**: [Scenario 5.1](#scenario-51---open-the-state-properties-dialog) is completed and the user wants to give the new state an existing name.

**Steps**:

1. The user presses the "OK" button.
2. An error message dialog is shown to the user.
3. The user presses the "OK" button in the error message dialog.
4. The state properties dialog is not closed.

### Scenario 5.5 - Cancel the addition of a new state

**Preconditions**: [Scenario 5.1](#scenario-51---open-the-state-properties-dialog) is completed and the user wants to cancel the addition of a new state.

**Steps**:

1. The user presses the "Cancel" button in the state properties dialog.
2. The state properties dialog is closed.
3. The new state is not added to the diagram canvas and the states list.

## Use case 6: Add a new choice-point

**Objective**: Add a new choice-point to the current diagram.

### Scenario 6.1 - Open the choice-point properties dialog

**Preconditions**: The user wants to add a new choice-point to the current diagram.

**Steps**:

1. The user presses the "Add Choice-Point" button in the toolbar.
2. The choice-point properties dialog is shown.

### Scenario 6.2 - Add choice-point with a unique name

**Preconditions**: [Scenario 6.1](#scenario-61---open-the-choice-point-properties-dialog) is completed and the user wants to give the new choice-point a unique name.

**Steps**:

1. The user fills in the unique choice-point name.
2. Optionally, the user fills in the question.

### Scenario 6.3 - Save the new choice-point

**Preconditions**: [Scenario 6.2](#scenario-62---add-choice-point-with-a-unique-name) is completed and the user wants to save the new choice-point.

**Steps**:

1. The user presses the "OK" button.
2. The choice-point properties dialog is closed.
3. The new choice-point is added to the diagram canvas and the choice-points list.

### Scenario 6.4 - Try to add choice-point with an existing name

**Preconditions**: [Scenario 6.1](#scenario-61---open-the-choice-point-properties-dialog) is completed and the user wants to give the new choice-point an existing name.

**Steps**:

1. The user presses the "OK" button.
2. An error message dialog is shown to the user.
3. The user presses the "OK" button in the error message dialog.
4. The choice-point properties dialog is not closed.

### Scenario 6.5 - Cancel the addition of a new choice-point

**Preconditions**: [Scenario 6.1](#scenario-61---open-the-choice-point-properties-dialog) is completed and the user wants to cancel the addition of a new choice-point.

**Steps**:

1. The user presses the "Cancel" button in the choice-point properties dialog.
2. The choice-point properties dialog is closed.
3. The new choice-point is not added to the diagram canvas and the choice-points list.

## Use case 7: Add a new interface

**Objective**: Add a new interface to the current diagram.

### Scenario 7.1 - Open the interface properties dialog

**Preconditions**: The user wants to add a new interface to the current diagram.

**Steps**:

1. The user presses the "Add Interface" button in the toolbar.
2. The interface properties dialog is shown.

### Scenario 7.2 - Add interface with a unique name

**Preconditions**: [Scenario 7.1](#scenario-71---open-the-interface-properties-dialog) is completed and the user wants to give the new interface a unique name.

**Steps**:

1. The user fills in the unique interface name.

### Scenario 7.3 - Save the new interface

**Preconditions**: [Scenario 7.2](#scenario-72---add-interface-with-a-unique-name) is completed and the user wants to save the new interface.

**Steps**:

1. The user presses the "OK" button.
2. The interface properties dialog is closed.
3. The new interface is added to the interfaces list.

### Scenario 7.4 - Try to add interface with an existing name

**Preconditions**: [Scenario 7.1](#scenario-71---open-the-interface-properties-dialog) is completed and the user wants to give the new interface an existing name.

**Steps**:

1. The user presses the "OK" button.
2. An error message dialog is shown to the user.
3. The user presses the "OK" button in the error message dialog.
4. The interface properties dialog is not closed.

### Scenario 7.5 - Cancel the addition of a new interface

**Preconditions**: [Scenario 7.1](#scenario-71---open-the-interface-properties-dialog) is completed and the user wants to cancel the addition of a new interface.

**Steps**:

1. The user presses the "Cancel" button in the interface properties dialog.
2. The interface properties dialog is closed.
3. The new interface is not added to the interfaces list.

## Use case 8: Select an interface

**Objective**: Select an interface

### Scenario 8.1 - Normal flow

**Preconditions**: No interfaces are selected and the user wants to select an interface.

**Steps**:

1. The user clicks on an interface in the interface list.
2. The selected interface is highlighted in the interface list.
3. All the messages of the selected interface are shown in the message list.

### Scenario 8.2 - Select a second interface

**Preconditions**: An interface is already selected and the user wants to select a second interface.

**Steps**:

1. The user clicks on an interface in the interface list.
2. The selected interface is highlighted in the interface list.
3. All the messages of the selected interface are shown in the message list.

## Use case 9: Deselect the interface

## Use case 10: Delete the selected interface

**Objective**: Delete the selected interface.

### Scenario 10.1 - Normal flow

**Preconditions**: An interface is selected and the user wants to delete the selected interface.

**Steps**:

1. The user clicks the "Delete" button in the toolbar.
2. The selected interface is deleted and the interface list is updated.
3. All the messages of the selected interface are deleted and the message list is updated.

## Use case 11: Add a new message

**Objective**: Add a new message to the current diagram for the selected interface.

### Scenario 11.1 - Open the message properties dialog

**Preconditions**: An interface is selected and the user wants to add a new message to the current diagram for the selected interface.

**Steps**:

1. The user presses the "Add Message" button in the toolbar.
2. The message properties dialog is shown.

### Scenario 11.2 - Save the message properties dialog

**Preconditions**: [Scenario 11.1](#scenario-111---open-the-message-properties-dialog) is completed and the user wants to save the message properties dialog.

**Steps**:

1. The user presses the "OK" button.
2. The message properties dialog is closed.
3. The new message is added to the diagram canvas and the message list.

### Scenario 11.3 - Add message with a unique name

**Preconditions**: [Scenario 11.1](#scenario-111---open-the-message-properties-dialog) is completed and the user wants to give the new message a unique name.

**Steps**:

1. The user fills in the unique message name.

### Scenario 11.4 - Try to add message with an existing name

**Preconditions**: [Scenario 11.1](#scenario-111---open-the-message-properties-dialog) is completed and the user wants to give the new message an existing name in the selected interface.

**Steps**:

1. The user presses the "OK" button.
2. An error message dialog is shown to the user.
3. The user presses the "OK" button in the error message dialog.
4. The message properties dialog is not closed.

### Scenario 11.5 - Cancel the addition of a new message

**Preconditions**: [Scenario 11.1](#scenario-111---open-the-message-properties-dialog) is completed and the user wants to cancel the addition of a new message.

**Steps**:

1. The user presses the "Cancel" button in the message properties dialog.
2. The message properties dialog is closed.
3. The new message is not added to the diagram canvas and the message list.

## Use case 12: Select a message

## Use case 13: Deselect the message

## Use case 14: Delete the selected message

## Use case 15: Add a new transition

**Objective**: Add a new transition to the current diagram.

### Scenario 15.1 - Add transition for each selected message

**Preconditions**: The user wants to add a new transition to the current diagram and one or more messages are selected.

**Steps**:

1. The user clicks the "Add Transition" button in the toolbar.
2. For each selected message, the transition is added to the diagram canvas and to the transition table.

## Use case 16: Select an element in the diagram canvas

## Use case 17: Deselect an element in the diagram canvas

## Use case 18: Update the properties of a selected diagram element

### Scenario 18.1 - Open the properties dialog

**Preconditions**: A single diagram element is selected and the user wants to update the properties of the selected diagram element.

**Steps**:

1. The user clicks the "Edit" button in the toolbar.
2. The properties dialog is shown.

## Use case 19: Delete the selected diagram elements


