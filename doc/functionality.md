## Editing a state diagram

_The State Diagram Editor is a tool that allows you to graphically edit a PlantUML state diagram. The following sections describe the functionality of the editor._

### Basic workflow

A basic workflow of the State Diagram Editor can be as follows:

1. Create a new state diagram.
2. Add interfaces.
3. Add messages for each interface.
4. Add states.
5. Add choice-points.
6. Add transitions.
7. Edit the diagram by selecting the elements and changing their properties.
8. Delete selected diagram elements that are no longer needed.
9. Save the diagram.
10. Open an existing diagram.

### Create a new diagram

When the application is started, the **default diagram** is loaded as given in the following PlantUML code:

```
@startuml
'== Formatting ==
hide empty description
skinparam Arrow {
  FontSize 9
}
skinparam State {
  FontSize 12
}

'== Default interfaces ==
!$Timer = Timer
!$Logical = Logical

'== Default messages ==
!$Timer_Timeout = Timeout
!$Logical_No = No
!$Logical_Yes = Yes

'== Interfaces ==

'== Messages ==

'== Component ==
state component as "Component Name" {
state START <<start>> #000000

'== States ==

'== Choice-points ==

'== Transitions ==
}
@enduml
```

The user is presented with the default diagram as shown below:

![](https://www.plantuml.com/plantuml/png/LL31IWCn4BtdAyOgU1BKcz2MbehWmJsuU_4ux4xRmMOc9BE8blwxsUmYQmvXtkFDUydR9CDelJ-vMrYju4MZHpEMGqRko1q1-M3Vq55g8mTZ5PS-MG96zB2DKR_Wx20lYjNyG_3aBZD1RMZqN_3mc1LZsZFjiJyPU4e93vI6pAkRXZrfRx22QSfSfHbMcgUFGGRvdZnUnIZkiHstH-vjvkTIUKAhFgYG6622nUuFLUXf0UT9LJVRzmQMorBAUWtNz-MCjkKpyvZTKRcbkw0iDgERY99uQAgG5xSXwNB3lm00)

The user can start editing the diagram by changing the name of the component.

The user can also create a new diagram, in which case the name of the component must be specified. This name is used to identify the component that the state diagram describes.

Suppose the name is `Node`, then again, the default PlantUML string is loaded but now with the component name set to `Node` as follows:

```
@startuml
'== Formatting ==
hide empty description
skinparam Arrow {
  FontSize 9
}
skinparam State {
  FontSize 12
}

'== Default interfaces ==
!$Timer = Timer
!$Logical = Logical

'== Default messages ==
!$Timer_Timeout = Timeout
!$Logical_No = No
!$Logical_Yes = Yes

'== Interfaces ==

'== Messages ==

'== Component ==
state component as "Node" {
state START <<start>> #000000

'== States ==

'== Choice-points ==

'== Transitions ==
}
@enduml
```

This is then rendered by the PlantUML server and displayed in the diagram canvas as shown below:

![Initial Diagram](https://www.plantuml.com/plantuml/png/LL31JiCm3BtdAyn0ueG4t93MQHC8YGCzq5uuMgstMInsbBX2CEtVITCUIWwH_VByNlosoJ3Qu4_k5geANZLwD6CvvCuTkISW7-m7UafTv62iuj8NIy287dOnwZUS7UH1iOP_2PxSPK5e38t-4nuUCsDoUw4z3YS3JodXWTBeUNNJiYST32gOgupLcjjQS_KvqY3ViyQR6CKzTjFqXBqlz5mgN-ZK1nKI0qomghMd5PpdjwRTVRImNfSeDXkulYzd4YihBCMVZyeTtGLbiGNSHfJ4Opu5lBWjIPzp_GC0)

### Selecting and deselecting diagram elements

Diagram elements - states, choice-points, and transitions - can be selected - and deselected - by clicking on them in the diagram canvas. Multiple elements can be selected in this way.

Selection is indicated as follows:

- Selected states and choice-points are indicated with a red bold border.
- Selected transitions are indicated with a red bold line.
- A selected `START` icon is colored red.

This is done in the PlantUML code as follows.

```
@startuml
' == Formatting ==
hide empty description
skinparam Arrow {
  FontSize 9
}
skinparam State {
  FontSize 12
}

' == Default interfaces ==
!$Timer = Timer
!$Logical = Logical

' == Default messages ==
!$Timer_Timeout = Timeout
!$Logical_No = No
!$Logical_Yes = Yes

'== Interfaces ==

'== Messages ==

'== Component ==
state component as "Node" {
state START <<start>> #FF0000

'== States ==
state Advertising #line:FF0000;line.bold

'== Choice-points ==

'== Transitions ==
START -[#FF0000,bold]-> Advertising
Advertising -[#FF0000,bold]-> Advertising : $Timer_Timeout

}
@enduml
```

This is then rendered by the PlantUML server and displayed in the diagram canvas as shown below:

![](https://www.plantuml.com/plantuml/png/VP4_JyD03CNt-nGcHMAX2DWeRTKAL8c13cqMX1YEn6qjSkVepkKF5TyT9vTAOI53uhD_VYzvcKMnGVQkCcSmcS22WxCYvBTwCZig4T3LyWKbnY9GBSJUn3VojGtMmJm4_e230LtqigPlX1lpqmFMOWN_0bVNIYItUzpOVINWC4QxnTXudfpcv93t0XFeAkqjMOzBrkgfmK3ldSQ35mmRMnotL_cdpZDzP1tns5CtiNsXWbtD7hs0ZP0jkSGC3jridSzNEOp7RJ3JAGmMYqkzabZwe5OgqVFo7ODGR18RLEHnbF3RfhvuvQhi5kzsJ0KEQoOlxNvgvy7wI4siRJEP3vyxq_D6u6KuxTkONlq_2ICuXcaqyndwKd_qBm00)

When a single element is selected - unless it is the `START` icon which has no properties - the properties can be edited in a properties dialog.

### Add an interface

Interfaces can be added to the list of interfaces by specifying the interface name, which needs to be a single word and unique.

When the interface is added, its name will appear in the list of interfaces and it will be added to the PlantUML code as follows:

```
!$Interface = Interface
```

A newly added interface is selected automatically.

### Add a message

A message is always associated with an interface. Therefore, when adding a message, the interface needs to be selected first.

When the interface is selected, the message name can be specified, which needs to be a single word and unique for the selected interface.

When a message is added, its name will appear in the list of messages and it will be added to the PlantUML code as follows:

```
!$Interface_Message = $Interface + ":" + Message
```

### Add a state

States can be added to the list of states by specifying the state name which needs to be a single word and unique.

Optionally, a display name can be specified, which can span multiple lines if necessary (indicated by the `\n` newline character). The display name does not need to be unique nor correlate to the state name, although this is normally the case.

When the state is added, its name will appear in the list of states, and it will be added to the PlantUML code as follows:

```
' == States ==
state Advertising
```

The `Advertising` state is then displayed in the diagram as shown below:

![Adding a state](https://www.plantuml.com/plantuml/png/LL71JiCm3BtdAyn0ueG4t93MQHK82GbweBrmcgBMwooQk4fS44pxzwL9fRKzkCxBUy-ElVMYdGocKxTP1g_iZ1OXsqAMgGCr26Xw-OC6VUse5sAh_3VPNZjj87UEV-6e80YjbFIFyAHECq8fMd19U7WCZ5Zi1VTww0J82hgzhj6FHQzkAZBe88Fu3-TtRgdMNK2cR2atwBrk5-BT67cG89coYysku00NF4E-HZ64c8pVvlqaw6DMG_dug9fDpnQjWFQmAhZ15HodkxBAFojOh-DiDnkulezVyXfdafmIEMz-q0dvCFH4U3umrNZNCrcvj50vRJsD2uZOIMtHDc5lPm00)

When the display name is specified, then the display name is used instead of the state name in the list of states and in the diagram. The PlantUML code would then be as follows:

```
' == States ==
state Advertising as "Advertising\nin Progress"
```

This is then displayed in the diagram as shown below:

![Adding a state](https://www.plantuml.com/plantuml/png/LL5VIyD037-_Jn6du9EWlWdhs504GVVW-Y88usYpBhXBZhjCqR7lxYqRhEt3DVdrzoVDJRFwfDkmSTTL1S-IWbSbxg2gt9fQ10nHVw75t2IAIi8kVn57dto0MKho0pi7HSYwe3-41xVl4HRg5OU4k_l2iB0dNFdjHe5OCQryW_aGUd5LKy045TYxzA_IKUCt1JbLGtd0d7qt42yFfspLJAmwsopdKk2vz92FWnZAUJH-6SnZq5ilmsNxgKP254PMy1b6Ssbn1BlJjqKzUwzXFBRTJYPmUMkFUTbEpEb4dhNVc9GoSMTMlVwJYI4cwLB97ntbZskX1c-Y4Ejvm3fvpgGaRDZUJP7RSgl_)

Note that no transitions are defined yet, so the `Advertising` state is not connected to any other state.

### Add a choice-point

Choice-points can be added to the list of choice-points by specifying the choice-point name which needs to be a single word and unique.

Also, a question must be specified, which can span multiple lines if necessary (indicated by the `\n` newline character). The question does not need to be unique nor correlate to the choice-point name, although this is normally the case.

When a choice-point is added, it will appear in the list of choice-points and in the diagram.

For example, the following line is added to the PlantUML code to add the `Whitelisted` choice-point:

```
' == Choice-points ==
state CP_Whitelisted as "Is Server\nWhitelisted?"
```

Note that for the name, the `CP_` prefix is added automatically, i.e. not part of the specified name.

The `Whitelisted` choice-point is then displayed in the diagram as shown below:

![Adding a choice-point](https://www.plantuml.com/plantuml/png/LP1VImCn3C3V-odY57mIr3TXcniJOQ13l0CH12btsHQy9aUJKtJikzlLFinxEFBdbr_QpjHyj25qxXmc4xYN6BmPyIPbRaij0eRUlg55RIBrHi9EFuXx7ts0UOpo1Ji7QP2jeX-46xS_0YhpXl-1g-j4_6sxmxKVEeE0gdw3UjXvSbPJG1aC9b2YL5j9IbUIejS31kbV74isZ6lVvEbIUppoESr7Q2JqmiW6Nc6qaXP7i2kzgfu_rp0UvwUOJk7qCdz5bgzmK1LwtdvYD5BYJI4MMw46BteXjYDmyVJ-iYN31rB3DkzTAbGOq_mRvrQNMxUZ8ggZPoKZuQpPknboEuJk5m00)

A newly added choice-point is selected automatically.

### Add a transition

To be able to add a transition, a source state (first state selected), a target state (second state selected), and a message must be selected.

When there is no transition between the selected source and target states yet, a new transition can be added. This transition will have the default connector `->`.

For example, the following line is added to the PlantUML code to add a transition from the `Advertising` state to the `CP_Whitelisted` choice-point when the "ConnectReq" message of the `RTx` interface is selected:

```
Advertising -> CP_Whitelisted : $RTx_ConnectReq
```

This will be displayed in the diagram as shown below:

![Adding a transition](https://www.plantuml.com/plantuml/png/NP7VIyD03CVVxw-8LV111kgROviR5M4F3baB8WZZQBFji9UhTwa_7FxlPkUXTNq8IR-VV1Doqy3QSsSRTGhZCTmwRpMpeOrKQcjg1BGjVq2DeVAcPUD8XMT3hVRQminxzmOx1T98N9XFX2lrrGCArep_WOjB8NwctU1QTms3nH3q1iD-vj59QIowZc4CAPD_2oVbmadskCT0OlAO4wDVwmfJzx9y5rrYqk-YTqzTvOu8ArxYYu2HFuDic4dyKvGASVFAsTOH4eCEaEM_rK9Rp62NgAASBKiOZU8j9nCuFezVsg0G9ivFzAn-HSyco94JaM-TgN3GEaFS0_FxrSFMC3OcCDPnWtc00htqFr5FkiwIKUar1SF6KRJfJOB1vD1l20VdKF8mKwIwiyqt)

A newly added transition is selected automatically allowing the transition to be edited immediately.

The connector can be changed by selecting a different connector from the list of available connectors; `Right`, `Left`, `Down`, and `Up`. Additionally, the length of an `Up` or `Down` transition can be elongated by entering an integer value larger than 1.

Any additional transitions that are created between the "Advertising" and "CP_Whitelisted" states result in messages being added. For example, the following line is added to the PlantUML code to add the `$RTx_ConnectedInd` message to the transition:

```
Advertising -> CP_Whitelisted : $RTx_ConnectReq\n$RTx_ConnectedInd
```

Note that the messages separated by a newline character and are displayed in this order as displayed in the diagram below:

![Adding a transition with messages](https://www.plantuml.com/plantuml/png/PP1FIyD04CNl-od6A7Wgg3TBMriYGWyMQG8Y5CgIJDl1x6pSdVZ7qk_k6XTDQWvXvkNttcxUr8jsqfXAdSDu37VM6Ir2l0sRsb69WAQM3oZH5uvg8SlAFnFNsca3C-Vi6-mL12DBHfy8r-hG0JBHWdtWyYeGFwVTuaOtbO11x_KMVT3KoLbE1cqZC8Ou1MrXmxgmONhwnY2yOyQS1Tr65wqxQlUzl6N-laujCnQon9TWJe8o_5EIFeFbdCiU5RL4AT_-Jc5DRHbPG7j8qjzjeGqci8zKbi-MEOn6RS6J2PnUj4-yObkC3rEaP-KhEY4Vcez4khDKuA2snD81quVruuu4A_A2PNk3kOSCNV2lkFFf9eb1kTFiISXo6zCv2GQJuxmX7FMrud_bA7LGK-IoCTKN)

### Add a self-transition

A self-transition is a transition where the source and target states are the same. Note that it is not possible to add a self-transition to a choice-point or to the `START` icon.

To be able to add a self-transition, only one state and the message needs to be selected.

When it is then indicated that a transition is to be added, the self-transition is added to the selected state which can then be edited in the same way as other transitions.

For example, the following line is added to the PlantUML code to add a self-transition to the `Advertising` state with the `$Timer_Timeout` message selected:

```
Advertising -> Advertising : $Timer_Timeout
```

Which is then displayed in the diagram as shown below:

![](https://www.plantuml.com/plantuml/png/PP5VIyCm5CNVyockLV1feBuvjhbH4VRWaBKWmc24zcuBDZSrkVMFm-_kjKPjPnzAxkdldAGdqy3QSsChTGhZCTmuRpMpeQrCQcTA1BGrlq69eV2cPkD8XKT3jVRQminxzm9x1M8apimxmgNww00PQyO-S7uXnFTkrxZHJSLWCGIznI2QEZh9ZKNNC8mXhaHRE1aNJbOFNnZ8EsRCYT5lTD6wetRRorlch-lK4M71ItmISoBAy4z9-WoMSofxLDGIfKBxEuMpjICa1XqWIN-dXRQOm3vIMJvRvZ0QjGLF9d1yrZxnY6qnGLQHdfNFwDa4QJuIwSwP0WUrCyGTCBrRt-yCOsK2OzcUO1uWGo_-5NK-NIKnAFUQWc7Zg8tfx0I3oM7U40xwMj6_SWuZkgFuVsvDhdcAL3Qs-WG0)

For self-transitions, the connector is always `->`. Looking at the diagram above, this means that we need to change the connector of the transition to the `CP_Whitelisted` choice-point to `Down` (or `Up`) to make room to display the messages in the self-transition as shown below:

![](https://www.plantuml.com/plantuml/png/PP7VI_im5CNVyrVSRx-2JmFrpR7LZOgm1uUi1H468xHtMx2vgScjFnp-xrvgr7RseUIUViv9UZ8Bh3stjbQdC9t2ZVDMCnlQoQJsfa90s_0RL1XARnesZbHuDDHehotClNSlS50WHkBSl2DSgeyUaBDc70Bd5q9yxNQDMztM31P3q3iCegb_9uMnw5g6ASILQ4iduzB9wW450td7Z0Kn-gqkEtVKRWTvg-9rapaYB7c5Js9EH1d_AicGmMf1rO2AMg9Kw7wdTBPnXCIW0oJPpxJK5XCuH2elvgi29fEku3I5_sVT4u_O5HDa5UbvzOoUJP3c8v7jdIbnr3X3t0EpkytztZ3M9Z1MtGaM0NBqubzJxzDL4eCAhoaODewwcDvEC1gbnu5ZE2fiJN_Q6MQaq1_5_trjSiypfAgrzIS0)

### Specifying the initial state transition

The initial state transition indicates the first state of the component.

For our example, by selecting the `START` icon and the `Advertising` state as the source and target states, a transition between them can be created. This transition is then specified as the initial state transition. Note that in this case, no messages are associated with the transition.

This is specified using the syntax in the PlantUML code as shown below:

```
START -> Advertising
```

Which is displayed in the diagram as shown below:

![](https://www.plantuml.com/plantuml/png/PPBVIyD03CVV-rV4AlWqKDySszoe27jmo5eGOJ2EDjiETxbwb_d3uVzksftQctqekTmdtwJVTEnPETwPRN8Emo7SMMSKiwQrd9ADhX3GrFm15VhIwPgrfSG_QwgLKmOcpjats2SWXSIv_aIuJhuwGCwACGOkhuGuTBl5bTfj6GnwhzRecvudPuKsQ7SCGmYHv6PMZZChqLE3WRo3nfGOtKgLRNN8tKTwy-9zcLaYB7cEBrASIgR_bqbZ1gifLH4LSccI-FPpIcjgIqWCoaEQ_Pvcoc0A-q3bnMHUm63G6ZmQmUb5-uGHMsEyH86ULA_eM7jnFX3PnkeIUxNLn1qmUrW-RZJZLdl6gfrWwY579_KBwbpTf46eS8gyRZRNoXpcwesYbfqOUd9trAKFHoukw9zbaKOitzJ_x5AMFqQgv8_x1W00)

The initial state transition can be changed like any other transition but only the connector can be changed as no messages are associated with the initial state transition.

There can only be one initial state transition. This means that if the initial state transition is changed, any previous initial state transition is removed.

### Select and edit a transition

A transition can be selected by clicking - approximately - on the line (see ["Selecting and deselecting diagram elements"](#selecting-and-deselecting-diagram-elements)).

When a single transition is selected, the properties panel is updated to show the connector information (if it is not a self-transition) and the messages that are associated with the transition (if it is not an initial state transition).

Messages can be added like described before or removed from the transition by selecting the messages from the list and removing them.

### Deleting diagram elements

All diagram elements can be deleted by first selecting them and then indicating that the elements should be deleted.

### Selection mask

The PlantUML server takes the PlantUML code and generates a PNG image of the diagram which is displayed in the diagram canvas. This means that the actual location of the elements in the diagram canvas is not known to the application.

To implement the selection of elements, a copy of the diagram is made in which the following is changed in the formatting section:
- All text for both states and arrows is made transparent by setting the font color to `#00000000`.
- The thickness of the arrows is increased to 8 to make them easier to click on.

Then, each element is given an identifier, starting at 1 (the `START` icon already has identifier 0) and in the order the element appears in the diagram.

This identifier is then used as the color of the element as follows:

```
#0000hh
```

Where `hh` is the hexadecimal representation of the identifier.

The following PlantUML code shows the changes for the earlier diagram:

```
@startuml
' == Formatting ==
hide empty description
skinparam Arrow {
  FontSize 9
  FontColor #00000000
}
skinparam State {
  FontSize 12
  FontColor #00000000
}

' == Default messages ==
!$Timeout = Timeout
!$No = No
!$Yes = Yes

' == Interfaces ==
!$RTx = RTx

' == Messages ==
!$RTx_ConnectReq = $RTx + ":" + "ConnectReq"
!$RTx_ConnectedInd = $RTx + ":" + ConnectedInd
!$RTx_DisconnectInd = $RTx + ":" + DisconnectInd

state component as "Node" {

state START <<start>> #000000

' == States ==
state Advertising #000001;line:000001
state Connecting #000002;line:000002
state ServerConnected as "Server\nConnected" #000003;line:000003

' == Choice-points ==
state CP_Whitelisted as "Is Server\nWhitelisted?" #000004;line:000004

' == Transitions ==
START -[#000004]-> Advertising
Advertising -[#000005,thickness=8]-> Advertising : $Timeout
Advertising -[#000006,thickness=8]-> CP_Whitelisted : $RTx_ConnectReq
CP_Whitelisted -[#000007,thickness=8]-> Connecting : $Yes
CP_Whitelisted -[#000008,thickness=8]up--> Advertising : $No
Connecting -[#000009,thickness=8]-> Advertising : $Timeout
Connecting -[#00000A,thickness=8]> ServerConnected : $RTx_ConnectedInd
ServerConnected -[#00000B,thickness=8]-> Advertising : $RTx_DisconnectInd\n$Timeout
ServerConnected -[#00000C,thickness=8]-> ServerConnected : $RTx_ConnectedInd
}
@enduml
```

This renders as follows:

![](https://www.plantuml.com/plantuml/png/ZPBVRzCm4CVV_LSS0Oa7L8br0xQmbfLCI7sWGcqaX5WrMSbjjPROmNRumRJ_7ISvjsxIIlGXFVi-z_NNvxiobcjRbmLx2PC9V5AwvDOAUUzMR2Do12mh-mToD9aMbHLAClCWPCKrBs6cjVe5ZmnSeRGhyHVXmYtIZSWU91e3vvHALA4qF7zDF_OKYAmijxWlSZ8-MjVvlCOxNXSMIZI6twDft3vxaOeILMrX0XIvlOLoouLoqRS60_SbZRcqgEzuvgkNwM-NZznVHCHdh-xpjucI4ZExn1yERIjUGHH7pNUNYlPXpESoFunJqXTS2vDrsuSgzhBEecdxbgcoKXAb1MuWMgWS8tZqoLKwMwPmUTa-ydJg6qdNQnjlN4JqBF-9sWhZNf_8a_U5a1XtCL5aV0UD0sZi3qRjjBPtRBrrUpToknkHm6aWS4hUaeqI6Oug9QGDB2PVRhzkXCL262yxD-2LWzG7BtuMY9-HUAgvDAAPvLQwwzBeEtLdFPg6hM11l8NUz228mK_VGVwju_lcO-YD5Ei1llXTKqmOdUMc-1XzlgwhqT3TGh50miCNn-zn29-jfuEdZM4mxApF-FgFm-E6WtyZlOMZEedJ-IyZJ-mAPLwNnJy0)

This image is not displayed in the diagram canvas but kept in memory.

Every time a new diagram is loaded or the current diagram is updated, the selection diagram is updated and the selection mask is recreated.

When the user clicks on the original diagram, the coordinates of the click are used to retrieve the color of the element at the same coordinates in the selection mask. If the color matches the color of an element in the original diagram, that element is selected, or deselected when the user clicks again on the same element.