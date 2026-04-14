# EcoEcon — Biological Early Warning Signals for Economic Crises

> What if we could predict financial crises the same way ecologists predict ecosystem collapse?

This project applies ecological network theory to economic systems — modeling the US economy as a food web where sectors are species, supply chains are predator-prey relationships, and financial crises are extinction cascades.

## Key Finding

Three biological early warning signals — the **Economic Biodiversity Index (EBI)**, keystone sector concentration, and spectral gap — all deteriorated before the 2008 financial crisis, with the EBI peaking in 2005 and declining continuously through the crash.

## Novel Metric: Economic Biodiversity Index (EBI)

The EBI quantifies systemic resilience using Shannon entropy applied to sector centrality distributions, penalized by keystone concentration. A declining EBI signals a fragile, monoculture-like economy vulnerable to cascade failure.

## Results

![Early Warning Signals](data/ecoceon_full_analysis.png)

![Keystone Sectors](data/keystone_sectors_2006.png)

## Methodology

- **Data**: BEA Input-Output Tables (68 sectors, 2002–2009)
- **Network**: Directed weighted graph of inter-sector monetary flows
- **Signals**: Betweenness centrality, spectral gap, Shannon entropy
- **Ecological analog**: Lotka-Volterra dynamics, keystone species theory, May's stability theorem

## Roadmap

- [x] Phase 1: EBI metric + sector dependency network
- [x] Phase 1: 2008 crisis early warning signals
- [ ] Phase 2: Critical slowing down from FRED time series
- [ ] Phase 3: ML model — GNN pre-trained on ecological collapse data
- [ ] Phase 4: Live real-time dashboard
- [ ] Phase 5: arXiv preprint

## References

- May, R.M. (1972). Will a large complex system be stable? *Nature*
- Scheffer et al. (2009). Early-warning signals for critical transitions. *Nature*
- Acemoglu et al. (2015). Systemic risk and stability in financial networks. *AER*

## Author

Abhinav Vaddi — DS / Economics / Biology
