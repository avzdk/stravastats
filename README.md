# stravastats

Henter data fra Strava og viser statistiske nøgletal


```mermaid
    classDiagram
        Strava <|-- StravaClient
        StravaClient "1" o-- "0..*" Activity 
        StatsGenerator "1" o-- "0..*"  Activity

        Activity: start_date_local
        Activity: name 
        Activity: distance  
        Activity: moving_time
        Activity: average_speed
        Activity: sport_type 
        
        Strava : getToken()
        Strava : exchange()
        Strava : getAthlete()
        Strava : getActivities()

        StravaClient : runningactivities()

        StatsGenerator : reset()
        StatsGenerator : filter()
        StatsGenerator : sort()
        StatsGenerator : basicstats()
```


## Token exchange
```mermaid
sequenceDiagram
    participant Browser
    participant Front
    participant App
    participant Strava
    Browser->>Front: Hent
    Front-->> Browser : Side
    Note right of Browser: User click login
    Browser->>Strava : autherize(clientId,redirect_url)
    Strava-->> Browser : Godkendelsesside
    Browser->>Strava : Ok
    Note right of Strava: Redirect
    Browser ->> App : exchange_token(authorization_code)
    App->>Strava: token(authorization_code)
    Strava-->>App: (refresh_token,access_token)
    App->>Strava : getActivities(access_token)
    Strava-->>App : Activities
    App-->>Browser : Stats
```