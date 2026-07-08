#!/usr/bin/make
DEBUG=
MAK=kibot.mak
CONFIG=../FP-GENERIC.kibot.yaml
SCH=FP-XY-DECOR-BOLD.kicad_sch
PCB=FP-XY-DECOR-BOLD.kicad_pcb
DEST=mfg-bot

all: erc_and_fab drc_and_fab cross dot minicross mix

clean: 
	rm -dr mfg-bot mfg-bot-cross mfg-bot-dot mfg-bot-minicross mfg-bot-mix

$(MAK): $(CONFIG)
	kibot -e $(SCH) -b $(PCB) -c $< -d $(DEST) -m $@

erc: $(MAK)
	$(MAKE) -f $(MAK) run_erc

drc: $(MAK)
	ls

sch_fab: $(MAK)
	$(MAKE) -f $(MAK) out_sch

pcb_fab: $(MAK)
	$(MAKE) -f $(MAK) out_pcb

erc_and_fab: $(MAK)
	$(MAKE) -f $(MAK) all_sch

drc_and_fab: $(MAK)
	$(MAKE) -f $(MAK) all_pcb

# Variant: Cross
cross: kibot-cross.mak
	$(MAKE) -f kibot-cross.mak all_pcb

kibot-cross.mak: $(CONFIG)
	kibot -e $(SCH) -b FP-XY-DECOR-BOLD-CROSS.kicad_pcb -c $< -d mfg-bot-cross -m $@

# Variant: Mix
mix: kibot-mix.mak
	$(MAKE) -f kibot-mix.mak all_pcb

kibot-mix.mak: $(CONFIG)
	kibot -e $(SCH) -b FP-XY-DECOR-BOLD-MIX.kicad_pcb -c $< -d mfg-bot-mix -m $@

# Variant: Dot
dot: kibot-dot.mak
	$(MAKE) -f kibot-dot.mak all_pcb

kibot-dot.mak: $(CONFIG)
	kibot -e $(SCH) -b FP-XY-DECOR-BOLD-DOT.kicad_pcb -c $< -d mfg-bot-dot -m $@

# Variant: Minicross
minicross: kibot-minicross.mak
	$(MAKE) -f kibot-minicross.mak all_pcb

kibot-minicross.mak: $(CONFIG)
	kibot -e $(SCH) -b FP-XY-DECOR-BOLD-MINICROSS.kicad_pcb -c $< -d mfg-bot-minicross -m $@

.PHONY: erc drc sch_fab pcb_fab erc_and_fab drc_and_fab all_variants cross dot minicross mix
