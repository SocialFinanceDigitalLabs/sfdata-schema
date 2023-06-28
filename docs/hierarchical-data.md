# Hierarchical Data

```xml
<Message>
    <Header>
        <CollectionDetails>
            <Collection>CIN</Collection>
        </CollectionDetails>
    </Header>
    <Children>
        <Child>
            <ChildIdentifiers>
            </ChildIdentifiers>
            <ChildCharacteristics>
                <Ethnicity>WBRI</Ethnicity>
                <Disabilities>
                    <Disability>HAND</Disability>
                    <Disability>HAND</Disability>
                    <Disability>HAND</Disability>
                </Disabilities>
            </ChildCharacteristics>
            <CINdetails> 
            </CINdetails> 
            <CINdetails> 
            </CINdetails> 

        </Child>
    </Children>
</Message>
```

id: sfdata-sample-hierarchical
version: 1.0.0
description: |
This is a sample file to demonstrate how to use the sfdata tool.

In this case we create a very simple schema in a single file.

Based on: https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1025196/2022_to_2023_CIN_Census_Specification.pdf

```yaml
id: dfe-cincensus-2022
version: 1.0.0
description: |
  This is a sample file to demonstrate how to use the sfdata tool
  to parse hierarchical data.

records:
  Message:
    path: Message
    fields:
      MessageID:
        type: string
        primary_key: true
        generator: metadata/filename # generate from filename found in metadata - could also be UID, sequence, ...
      Collection:
        type: categorical
        path: Header/CollectionDetails/Collection
      Year:
        type: gYear
        path: Header/CollectionDetails/Year
      ReferenceDate:
        type: date
        path: Header/CollectionDetails/ReferenceDate
      SourceLevel:
        type: categorical
        path: Header/Source/SourceLevel

  Child:
    path: Message/Children/Child
    fields:
      MessageID:
        type: string
        primary_key: true
        foreign_keys:
          - Message.MessageID
      LAchildID:
        type: string
        primary_key: true
      UPN:
        type: string
      FormerUPN:
        type: string
      UPNunknown:
        type: string    
      PersonBirthDate:
        type: gDate
      ExpectedPersonBirthDate:
        type: gDate
      GenderCurrent:
        type: int
      PersonDeathDate:
        type: gDate
      Ethnicity:
        type: EthnicityType

  ChildDisabilities:
    path: Message/Children/Child/Disabilities/Disability
    fields:
      LAchildID:
        type: string
        primary_key: true
        foreign_keys:
          - Child.LAchildID      
      Disability:
        type: DisabilityType
        primary_key: true
        path: .

  CINdetails:
    path: Message/Children/Child/CINdetails
    fields:
      LAchildID:
        type: string
        primary_key: true
        foreign_keys:
          - Child.LAchildID
      CINreferralDate:
        type: gDate
        primary_key: true
    
types:
  DisabilityType:
    restriction:
      base: string
      enumeration:
        - HAND
        - LEG
        - HEAR
        - SEE
        - SPEECH
        - LEARN
        - BEHAV
        - MENTAL
        - PHYS
        - MED
        - OTHER
        - NONE
 


```
