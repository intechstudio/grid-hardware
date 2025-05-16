#!/usr/bin/make
DEBUG=
MAK=kibot.mak
CONFIG=../PCBA-MOTHERBOARD.kibot.yaml
SCH=FP-PBF4-CLASSIC.kicad_sch
PCB=FP-PBF4-CLASSIC.kicad_pcb
DEST=mfg-bot

all: erc_and_fab drc_and_fab

clean: 
	rm -dr mfg-bot

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

.PHONY: erc drc sch_fab pcb_fab erc_and_fab drc_and_fab
