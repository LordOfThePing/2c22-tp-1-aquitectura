ping-stress: 
	npm run scenario ping/stress node >ping/stress.txt
ping-multi-stress: 
	npm run scenario ping/stress node >ping/multi-stress.txt
ping-endurance: 
	npm run scenario ping/endurance node >ping/endurance.txt
ping-multi-endurance: 
	npm run scenario ping/endurance node >ping/multi-endurance.txt
ping-spike:
	npm run scenario ping/spike node >ping/spike.txt
ping-multi-spike: .
	npm run scenario ping/spike node >ping/multi-spike.txt
ping-breakpoint: 
	npm run scenario ping/breakpoint node >ping/breakpoint.txt
ping-multi-breakpoint: 
	npm run scenario ping/breakpoint node >ping/multi-breakpoint.txt

sync-stress: 
	npm run scenario sync/stress node >sync/stress.txt
sync-multi-stress: 
	npm run scenario sync/stress node >sync/multi-stress.txt
sync-endurance: 
	npm run scenario sync/endurance node >sync/endurance.txt
sync-multi-endurance: 
	npm run scenario sync/endurance node >sync/multi-endurance.txt
sync-spike:
	npm run scenario sync/spike node >sync/spike.txt
sync-multi-spike: .
	npm run scenario sync/spike node >sync/multi-spike.txt
sync-breakpoint: 
	npm run scenario sync/breakpoint node >sync/breakpoint.txt
sync-multi-breakpoint: 
	npm run scenario sync/breakpoint node >sync/multi-breakpoint.txt

async-stress: 
	npm run scenario async/stress node >async/stress.txt
async-multi-stress: 
	npm run scenario async/stress node >async/multi-stress.txt
async-endurance: 
	npm run scenario async/endurance node >async/endurance.txt
async-multi-endurance: 
	npm run scenario async/endurance node >async/multi-endurance.txt
async-spike:
	npm run scenario async/spike node >async/spike.txt
async-multi-spike: .
	npm run scenario async/spike node >async/multi-spike.txt
async-breakpoint: 
	npm run scenario async/breakpoint node >async/breakpoint.txt
async-multi-breakpoint: 
	npm run scenario async/breakpoint node >async/multi-breakpoint.txt

heavy-stress: 
	npm run scenario heavy/stress node >heavy/stress.txt
heavy-multi-stress: 
	npm run scenario heavy/stress node >heavy/multi-stress.txt
heavy-endurance: 
	npm run scenario heavy/endurance node >heavy/endurance.txt
heavy-multi-endurance: 
	npm run scenario heavy/endurance node >heavy/multi-endurance.txt
heavy-spike:
	npm run scenario heavy/spike node >heavy/spike.txt
heavy-multi-spike:
	npm run scenario heavy/spike node >heavy/multi-spike.txt
heavy-breakpoint: 
	npm run scenario heavy/breakpoint node >heavy/breakpoint.txt
heavy-multi-breakpoint: 
	npm run scenario heavy/breakpoint node >heavy/multi-breakpoint.txt

rebuild-single: 
	docker compose stop -t0
	docker compose up -d 
	docker compose ps

rebuild-multi: 
	docker compose stop -t0
	docker compose up -d --scale node=3
	docker compose ps

sync-single:
	make rebuild-single
	make async-stress
	make rebuild-single
	make async-endurance
	make rebuild-single
	make async-spike