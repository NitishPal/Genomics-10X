import gzip
import os

# make a list for all barcodes in BarCode_list
BarCode_list = []
CellBarcode = input("Enter cell-barcode file: ")
CBl = open(CellBarcode, 'r')
for i in CBl:
	BarCode_list.append(i.strip())

# Get R1 and R2 files
UMI_seq = input("Enter R1 (i7+i5+Poly(T)) file of 10X Genomics V2: ")
R1 = gzip.open(UMI_seq, 'r')

cDNA_seq = input("Enter R2 (cDNA_seq) file of 10X Genomics V2: ")
R2 = gzip.open(cDNA_seq, 'r')

c = 0

# with open("final"+os.path.splitext(cDNA_seq)[0],'a+',encoding = 'utf-8') as outfile:
fastq_row = []
for l1, l2 in zip(R1, R2):
	c = c + 1
	l1 = l1.decode("utf-8").strip()[:16]
	l2 = l2.decode("utf-8").strip()

	if len(fastq_row) < 4:
		pass
	else:
		fastq_row = []	
	
	if c%4 == 1 or c%4 == 3:
		l2 = l2+'\n'
		# print(l1)
		fastq_row.append(l2)

	# If the read is present or not present; both cases something has to be added to the list
	elif c%4 == 2 and l1 in BarCode_list:
		seq = l1+l2+'\n'
		fastq_row.append(seq)
		# print(seq)
	elif c%4 == 2 and l1 not in BarCode_list:
		fastq_row.append(l2)

	elif c%4 == 0:
		ql = l1+l2+'\n'
		# print(ql)
		fastq_row.append(ql)

	# print(fastq_row)

	if len(fastq_row) == 4 and len(fastq_row[1]) > 88:
		with open("final_"+os.path.splitext(cDNA_seq)[0],'a+',encoding = 'utf-8') as outfile:
			for i in fastq_row:
				outfile.write(i)
			fastq_row = []
		# print(n)
