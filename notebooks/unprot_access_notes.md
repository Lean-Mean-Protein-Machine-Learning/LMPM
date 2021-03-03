# Keywords:
### When under the "UniprotKB" search bar (fields I've seen):
* Looking for human proteins:
	* `reviewed:yes AND organism:"Homo sapiens (Human) [9606]" AND proteome:up000005640`
* Looking for secreted proteins:
	* `locations:(location:"Secreted [SL-0243]") AND reviewed:yes`
* Looking for mammalian
	* `taxonomy:"Mammalia [40674]" AND reviewed:yes`

### Example querries sorting by "cellular component":
* Combining mammal and secreted:
	* `taxonomy:"Mammalia [40674]" AND locations:(location:"Secreted [SL-0243]") AND reviewed:yes`
* combining mammal and membrane:
	* `taxonomy:"Mammalia [40674]" AND locations:(location:"Membrane [SL-0162]") AND reviewed:yes`
* combining mammal and cytoplasm:
	* `taxonomy:"Mammalia [40674]" AND locations:(location:"Cytoplasm [SL-0086]") AND reviewed:yes`