# ScoringEngine-RandomIps
A repo to help us configure random IP addresses for scoring engine workers during a competition

## About
For RITSEC hosted competitions, we use an opensource [scoring engine](https://github.com/scoringengine/scoringengine).
We usually set up several workers to actually run all the checks. The checks are usually run on the same network at the Redteam/Whiteteam infrastructure so that the Blueteams cannot tell the difference between Redteam and the Scoring engine. This fails when the scoring engine is always using the same IP addresses because the blue teams can figure out the IPs. This repo aims to fix this by giving the scoring engine workers a random IP address whenever it is run.

## Usage
This program requires [detcord](https://github.com/micahjmartin/detcord) to interact with the hosts