# Class structure of the test System

## Core functionality
This is the class diagram for the main core functionality

```mermaid
erDiagram
    unit_test ||--o{ testController : uses
    config_yaml ||--o{ testController : programs
    testController ||--o{ dutSession : uses
    testController ||--o{ rackController : uses
    testController ||--o{ powerController : uses
    testController ||--o{ log : uses
    testController ||--o{ commonRemote : uses
    testController ||--o{ outbound : uses
```

## Rack Controller Overview

ClassName: rackController.py

```mermaid
erDiagram
    testController ||--o{ rackController : uses
    rackController }|..|{ rack : "uses..n"
    rack }|..|{ slot : "uses..n"
```

## Console Session Overview

```mermaid
erDiagram
    testController ||--|| deviceManager : has
    deviceManager ||--|{ device : has
    device ||..o{ serial : uses
    device ||..o{ ssh : uses
    device ||..o{ telnet : uses
```

## Test Controller Overview

```mermaid
erDiagram
    testController ||--o{ videoControl : uses
    videoControl ||--o{ stormVideo : uses
    videoControl ||--o{ magicVideo : uses
    videoControl ||--o{ FrankentienVideo : uses
```

## Power Controller Overview

```mermaid
erDiagram
    testController ||--|| deviceManager : has
    deviceManager ||--|{ device : has
    device ||--o{ powerControl : has
    powerControl ||..|{ Kara : uses
    powerControl ||..|{ olimex : uses
    powerControl ||..|{ s20 : uses
    powerControl ||..|{ HS100 : uses
    powerControl ||..|{ SLP : uses
```

## Webpage Controller Overview

```mermaid
erDiagram
		testController ||--o{ webpageController : uses 
		webpageController ||--o{ webPageConfig : uses
		webpageController ||--o{ seleniumDriver : uses
		seleniumDriver ||--o{ selenium : uses
```