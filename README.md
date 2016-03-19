# GMO-Gametheory-Simulation
Game simulation for whether a company willing to sell GMO food

### Complex version
Considering in the real situation, there are much more factors involved than the numbers of other companies selling GMO food. The threshold level should also change over time with the changing circumstances. I create this complex version so it is more close to the real life situation, and I will further deep into the details in the changing market structure. The rules are rather complicated, but with following:

1. Every companies as the beginning has a base threshold, a pure threshold to consider the number of other companies selling GMO food ignoring any other factors just like the simple version. The threshold will be sampled from reversed exponential distribution, because the more other companies selling GMO, the more likely a company want to involve.
The actual threshold will be updated based on the following three factors: 
  1. Capital. Each company has different size. The bigger a company is, the more likely this company want to involve, because they can make more money and more capable for risk resistance. The sizes will be sampled from exponential distribution with range of 1 - 499 million dollars, meaning that there are by far less big companies than small businesses, because, sadly, in the real life that is how wealth distributed. 
  2. Cognitive biases. Each company has different culture, some company managers are risk averse while others are risk seeking. Risk seeking people will more likely to sell GMO food than the risk averse, but it is not a false dichotomy, so I scale them from 1 to 5, close to 1 means risk averse, 5 means risk seeking. This data will be sampled from uniform distribution. 
  3. Drug quality (GMO food quality). The higher GMO food quality a company has, the less risk for that company, and therefore the more confident that company is to sell them in the market. Drug quality is also scaled from 1 to 5, 1 means low quality, 5 means high quality. This data will also be sampled from uniform distribution. 
  
Here is the formula to calculate the actual threshold:
```
Actual Threshold = Pure threshold - (capital / captial weight) -(bias - 3) * bias effect-(quality - 3) -quality effect
```
Constants
* Capital weight is 10, meaning that for each 10 millions dollar a company has, the actual threshold will be 1 point lower
* Bias effect is 25, meaning that if a company has highest risk seeking index (5), then it will lower the actual threshold by (5 - 3) * 10 = 50 points. If a company has lowest risk seeking index (1), it will lower the actual threshold by (1 - 3) * 10 = -50, so it will higher the actual threshold.
* Quality effect is 25, and it work the same way as bias effect.

Still confused?

Here is an example: Let’s say a company has 300 pure threshold. If this company has capital of 490 million dollars,  it will lower the actual threshold by (490 / 10) = 49 points, so threshold will be 251. If this company is risk averse (it has 1 as index), it will has (1 - 5) * 25 = 50 effect, so the actual threshold now become 251 + 50 = 301. If this company has highest drug quality, let’s say 5, then it will lower the threshold by (5 - 3) * 25 = 50, so at the end the threshold become (301 - 50) = 251. 

* We need to update these 3 factors over time. They all need to be update for each period (if there is 100 seasons in total, then it will be updated 100 times, a company will have update regardless whether they sell GMO food in the past season, because even if they are not selling GMO food, they will sell other products, which may turn out to influence whether they sell GMO food). Here are the rules for updating:
  1. Capital. Depend on the size of the company and their luck:
    1. If a company occupied more than 1% of market share, they have 50% chance to make 20 million dollars or lose 18 million dollars. 
    2. If a company occupied 0.5% - 1% of market share, they either make 10 million dollars or lose 8 million dollars
    3. For more than 0.2% - 0.5% market share, they either make 5 million dollars or lose 5 million dollars
    4. For lower than 0.2%, they either make 3 millions or lose 3 millions
    5. Special Note: If a company run out of money, they will not be able to return to the market. 
  2. Cognitive bias. If a company accumulated make more than 50 million dollars, that company will become more risk seeking, so the scale will increase one. If a company accumulated lose 50 million dollars, it will become risk averse and scale will decrease one.
  3. Drug Quality. If a company accumulated make more than 100 million dollars, they will choose to invest 100 million dollars to upgrade their drug quality. Their capital will decrease 100 million dollars but their drug quality will increase by 1 (There is not upper bound for technology). If a company accumulated lose more than 100 million dollars, their can not maintain their drug quality, so it will decrease by one. 
  
Each change in cognitive bias or drug quality will initialize the accumulated wealth.
