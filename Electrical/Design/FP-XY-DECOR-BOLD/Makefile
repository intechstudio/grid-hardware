#!/usr/bin/make
DEBUG=
MAK=kibot.mak
CONFIG=../FP-GENERIC.kibot.yaml
SCH=FP-XY-DECOR-BOLD.kicad_sch
PCB=FP-XY-DECOR-BOLD.kicad_pcb
DEST=mfg-bot

all: erc_and_fab drc_and_fab cross mix

clean: 
	rm -dr mfg-bot mfg-bot-cross mfg-bot-mix

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
cross: MAK=kibot-cross.mak
cross: PCB=FP-XY-DECOR-BOLD-CROSS.kicad_pcb
cross: DEST=mfg-bot-cross
cross: drc_and_fab

# Variant: Mix
mix: MAK=kibot-mix.mak
mix: PCB=FP-XY-DECOR-BOLD-MIX.kicad_pcb
mix: DEST=mfg-bot-mix
mix: drc_and_fab

.PHONY: erc drc sch_fab pcb_fab erc_and_fab drc_and_fab all_variants cross mix
