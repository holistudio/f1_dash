# Notes on Pit-stop time cost and recovery analysis 

**Pit-stop time**
- 2 second stationary stop
- 18-30 seconds total pit loss time
- clean air or traffic when they exit is huge

## Section 1: How a pit stop costs—or saves—a race position

Different tracks have different pit lane lenght => different pit-stop times

### Story 1: The mechanics of position loss from qualifying to finish

P4 car is 2 seconds behind
    Alex is at P3
        P2 is 1.5 seconds ahead

Alex pits in Lap 18 as planned
- 22 second total pit-loss time
    - P4 car is now ahead 24 seconds
    - P2 car is now ahead 25.5 seconds
    - Other cars may also be ahead

**Gap to Rival** how many seconds is car behind you

Position loss formula: `**Gap to Rival** < **Pit-stop time**`

Basic rule-of-thumb: Big gap to rival, OK to pit-stop
- even better but rare: rival pits in the next lap and you end up back in the lead AND with the same Gap to Rival by the time that rival leaves the pit *re-joining onto the track*

### Story 2: Position loss despite a fast stop—the undercut vulnerability

Tire degradation can be inferred by other teams based on eroding lap times
- other teams can anticipate when you will make a pit-stop
- then they make a pit-stop one lap earlier
- soft tire warmup take 1-2 sectors and then delivers **1.5-2 seconds per lap** advantage compared to other drivers' worn out tires.
- then that means the lead car gains even more of a lead after you pit.
- oh and you also have cold tires when you re-join, so you'll lose more time to get the tires warmed up

Then there's three other confounding factors:
- hard tires: should you change into hard tires, it'll take even more than 1-2 sectors to warm up (generally a full lap)
- you exit and re-join into traffic/dirty air
- certain tracks basically make overtaking impossible so a pit is a guaranteed loss

### Story 3: The well-timed stop that preserves position

Gap management: basically staying far ahead of rivals and sorta anticipating they will also need to pit and allow you to regain position regardless

Tire offset strategy: based on trials with different tires during practice/qualifying, an advantage may appear where you can expect your driver to overtake if they switch to a preferred tire sooner in the pit-stop

Safety car (SC) exploitation: safety car enables a free pit stop

## Section 2: Case studies in pit-stop failure and success

OK so basically 3 giant screw ups where the pit stop loss time was greater than normal
- Monaco 2016, Ricciardo is **stationary** for around 10-12 seconds (typical stationary time is 2 seconds)

Qatar 2025: McLaren had two drivers in P1 and P2. even though everyone else pitted during a safety car, McLaren feared a double-stack delay and decided to keep cars out for longer.

Hungary 2019: Hamilton starts at P3
- Verstappen tries to undercut with early pit-stop
- Mercedes lets Hamilton run six more laps
- At lap 48 Hamilton is 5 second behind Verstappen
- **Hamilton pits again**
- Hamilton rejoins with 19 seconds behind Verstappen
- But the rival car behind is 40 seconds behind Hamilton
- The pit stop essentially didn't risk losing P3, so it was a free pitstop/pit window.
- Supposedly, there's clean air in front further enabling Hamilton to speed up and catch Max
- Hamilton finishes P1

## Section 3: The strategic framework behind pit-stop decisions

### Qualitative frameworks shape how strategists think

Pit windows <==> Tire degradation
- how tires perform contributes to how the pit stops are planned/timed

Tire degradation phases
- warm-up / grip building
- stabilization / peak performance
- degradation / drop-off in acceleration: **generally sudden drop like a cliff**

Different tracks have different opportunities and barriers
- different opportunities to overtake/passing
- different opportunities for DRS
- different barriers in terms of traffic/dirty air

These above factors then have implications on different undercut or overcut strategies
- if you think you can get a fresh tire advantage, undercut
- if you think your tires will degrade slowly in a specific track or others will take very long to warm up the tires, maybe overcut and stay out longer

### Quantitative models provide the mathematical foundation

`Pit loss time = Entry time + Stationary time + Exit time - Track sector time`
- This is generally tracked during free practice

Monte Carlo simulations help with planning
- Safety car probability models are a big deal as these can be moment for free pit stop

## Section 4: The dashboard ecosystem informing pit-stop strategy

- Pit Window Estimates based on:
   - Tire compound
   - Lap times
   - Gap spread
   - Safety Car and Yellow Flag impacts
- Undercut Threat based on:
   - Gaps
   - Average pit loss
   - Tire performance
- Battle Forecast predicts laps until a cars behind are within striking distance


### Pre-race planning dashboards 

(Source: Analyst-Inferred) 

Typically include:
- Tire compound performance projections showing expected lap time versus stint length
- Crossover point charts identifying when softer compounds become slower than harder
- Strategy scenario comparisons (one-stop versus two-stop versus three-stop projected race times)