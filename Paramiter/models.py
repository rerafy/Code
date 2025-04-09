from django.db import models

# Create your models here.
import math
import cmath
import numpy as np

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=[
        ('External grid', 'กริด'),
        ('CB', 'เบรกเกอร์'),
        ('Recloser', 'รีโคลสเซอร์'),
        ('Fuse', 'ฟิวส์'),
        ('LINE', 'สายส่ง'),
        ('LOAD', 'โหลด'),
    ])

    icon = models.ImageField(upload_to='icons/', null=True, blank=True)

    def __str__(self):
        return self.name


#ข้อมูลหม้อแปลง
Vbase_22kV = 22  # แรงดันพิกัด (kV)
Un_22kV = Vbase_22kV * 1000  # แปลงเป็น V
I_SC_3P = 4.466 # กระแสฟอลต์ 3 เฟสฟอลต์
Sbase_22kV = 100 # กำลังไฟฟ้า Base
R1_PU = 0.08523  # Resistance1 ของระบบหม้อแปลง (ohm)
X1_PU = 0.58138  # Reactance1 ของระบบหม้อแปลง (ohm)
R2_PU = 0.08555  # Resistance2 ของระบบหม้อแปลง (ohm)
X2_PU = 0.58261  # Reactance2 ของระบบหม้อแปลง (ohm)
R0_PU = 0.01769  # Resistance0 ของระบบหม้อแปลง (ohm)
X0_PU = 0.30910  # Reactance0 ของระบบหม้อแปลง (ohm)
# Sbase_22kV = I_SC_3P * np.sqrt(3) * Vbase_22kV  #กำลังไฟฟ้า Base
Zbase_22kV = Vbase_22kV **2 / Sbase_22kV #หา Z Base 22 kV 
Ibase_22kV = Sbase_22kV / (cmath.sqrt(3) * Vbase_22kV) #หา I(phase) Base 22 kV
# Impedance Ratio
R1_X1_PU = R1_PU / X1_PU 
Z2_Z1_PU = complex(R2_PU, X2_PU)/complex(R1_PU, X1_PU)
X0_X1_PU = X0_PU / X1_PU  
R0_X0_PU = R0_PU / X0_PU 
Z1_PU = complex(R1_PU, X1_PU)
Z0_PU = complex(R0_PU, X0_PU)
R_im = 40 #40 ohm
R_im_PU = (R_im)/( Zbase_22kV) 
Z_im_PU = complex(R_im_PU, 0)
# แสดงผล impedance ของระบบหม้อแปลง 
print (Sbase_22kV)
print (Zbase_22kV)
print (R1_X1_PU)
print (abs(Z2_Z1_PU))
print (X0_X1_PU)
print (R0_X0_PU)
#ค่ากระแสฟอลต์ 3 เฟสหลังหม้อแปลง
Ifault_3P_PU_TR = (1) / (Z1_PU) #ค่ากระแสฟอลต์ 3 เฟส (pu) หลังหม้อแปลง
Ifault_3P_TR = abs(Ifault_3P_PU_TR) * Ibase_22kV  #ค่ากระแสฟอลต์ 3 เฟส (Actual)หลังหม้อแปลง
print (Ifault_3P_TR)
#ค่ากระแสฟอลต์  SLG หลังหม้อแปลง
Ifault_1P_PU_TR = (3) / ((2 * Z1_PU) + Z0_PU)     #ค่ากระแสฟอลต์ 1 เฟส (pu) หลังหม้อแปลง
Ifault_1P_TR = abs(Ifault_1P_PU_TR) * Ibase_22kV  #ค่ากระแสฟอลต์ 1 เฟส (Actual)หลังหม้อแปลง
print (Ifault_1P_TR)
#ค่ากระแสฟอลต์  SLG หลังหม้อแปลง 40 ohm
Ifault_1P_PU_TR_40  = (3) / ((2 * Z1_PU) + Z0_PU + (Z_im_PU))     #ค่ากระแสฟอลต์ 1 เฟส (pu) หลังหม้อแปลง
Ifault_1P_TR_40  = abs(Ifault_1P_PU_TR_40) * Ibase_22kV  #ค่ากระแสฟอลต์ 1 เฟส (Actual)หลังหม้อแปลง
print (Ifault_1P_TR_40 )

#ข้อมูลสายระบบจำหน่าย node 1 
R1_km = 0.2106598  # Resistance1 ของระบบจำหน่าย(ohm/km)
X1_km = 0.2985855  # Reactance1 ของระบบจำหน่าย (ohm/km)
R0_km = 0.402942  # Resistance0 ของระบบจำหน่าย (ohm/km)
X0_km = 1.857875  # Reactance0 ของระบบจำหน่าย (ohm/km)
Length_of_Line = 1.21 # ระยะทางสายส่ง km
R1L_PU = (R1_km * Length_of_Line )/( Zbase_22kV * 1.1 )   # Resistance1 ของระบบจำหน่าย (pu)
X1L_PU = (X1_km * Length_of_Line )/( Zbase_22kV * 1.1 )   # Reactance1 ของระบบจำหน่าย (pu))
R0L_PU = (R0_km * Length_of_Line )/( Zbase_22kV * 1.1 )  # Resistance0 ของระบบจำหน่าย (pu)
X0L_PU = (X0_km * Length_of_Line )/( Zbase_22kV * 1.1 )  # Reactance0 ของระบบจำหน่าย (pu)
Z1L_PU = complex(R1L_PU, X1L_PU)
Z0L_PU = complex(R0L_PU, X0L_PU)
#ค่ากระแสฟอลต์ 3 เฟส
Ifault_3P_PU = (1) / (Z1_PU + Z1L_PU) #ค่ากระแสฟอลต์ 3 เฟส (pu)
Ifault_3P = (abs(Ifault_3P_PU)) * Ibase_22kV  #ค่ากระแสฟอลต์ 3 เฟส (Actual)
#ค่ากระแสฟอลต์  SLG หลังหม้อแปลง
Ifault_1P_PU = (3) / ( (2 * Z1_PU)+ (2 * Z1L_PU)+ Z0_PU)     #ค่ากระแสฟอลต์ 1 เฟส (pu) หลังหม้อแปลง
Ifault_1P = abs(Ifault_1P_PU) * Ibase_22kV  #ค่ากระแสฟอลต์ 1 เฟส (Actual)หลังหม้อแปลง
#ค่ากระแสฟอลต์  SLG หลังหม้อแปลง 40 ohm
Ifault_1P_PU_40  = (3) / ( (2 * Z1_PU)+ (2 * Z1L_PU)+ Z0_PU + Z_im_PU )     #ค่ากระแสฟอลต์ 1 เฟส (pu) หลังหม้อแปลง
Ifault_1P_40  = abs(Ifault_1P_PU_40) * Ibase_22kV  #ค่ากระแสฟอลต์ 1 เฟส (Actual)หลังหม้อแปลง

print (abs(Ifault_3P_PU))
print (Z1_PU+Z1L_PU)
print (R1L_PU,R1_km * Length_of_Line )
print (X1L_PU,X1_km * Length_of_Line)
print (R0L_PU,R0_km * Length_of_Line)
print (X0L_PU,X0_km * Length_of_Line)
print (abs(Ifault_3P_PU))
print (Ifault_3P)
print (Ifault_1P)
print (abs(Z1_PU))
print (abs(Z1L_PU))


#ข้อมูลสายระบบจำหน่าย node 2 
R1_km_N2 = 0.640334  # Resistance1 ของระบบจำหน่าย(ohm/km)
X1_km_N2 = 0.4862455  # Reactance1 ของระบบจำหน่าย (ohm/km)
R0_km_N2 = 0.8213003 # Resistance0 ของระบบจำหน่าย (ohm/km)
X0_km_N2 = 1.606294  # Reactance0 ของระบบจำหน่าย (ohm/km)
Length_of_Line_N2 = 0.28 # ระยะทางสายส่ง km
R1L_PU_N2 = (R1_km_N2 * Length_of_Line_N2 )/( Zbase_22kV * 1.1 )   # Resistance1 ของระบบจำหน่าย (pu)
X1L_PU_N2 = (X1_km_N2 * Length_of_Line_N2 )/( Zbase_22kV * 1.1 )   # Reactance1 ของระบบจำหน่าย (pu))
R0L_PU_N2 = (R0_km_N2 * Length_of_Line_N2 )/( Zbase_22kV * 1.1 )  # Resistance0 ของระบบจำหน่าย (pu)
X0L_PU_N2 = (X0_km_N2 * Length_of_Line_N2 )/( Zbase_22kV * 1.1 )  # Reactance0 ของระบบจำหน่าย (pu)
Z1L_PU_N2 = complex(R1L_PU_N2, X1L_PU_N2)
Z0L_PU_N2 = complex(R0L_PU_N2, X0L_PU_N2)
#ค่ากระแสฟอลต์ 3 เฟส
Ifault_3P_PU_N2 = (1) / (Z1_PU + Z1L_PU_N2 + Z1L_PU) #ค่ากระแสฟอลต์ 3 เฟส (pu)
Ifault_3P_N2 = (abs(Ifault_3P_PU_N2)) * Ibase_22kV  #ค่ากระแสฟอลต์ 3 เฟส (Actual)
print (abs(Ifault_3P_PU_N2))
print (Z1_PU+Z1L_PU_N2)
print (R1L_PU_N2,R1_km_N2 * Length_of_Line )
print (X1L_PU_N2,X1_km_N2 * Length_of_Line)
print (R0L_PU_N2,R0_km_N2 * Length_of_Line)
print (X0L_PU_N2,X0_km_N2 * Length_of_Line)
print (abs(Ifault_3P_PU_N2))
print (Ifault_3P_N2)
print (abs(Z1_PU))
print (abs(Z1L_PU_N2))





# ฟังก์ชันคำนวณข้อมูลสายส่งเป็น pu
def get_line_parameters(length_km, R_km, X_km, Zbase, factor=1.1):
    R_line_PU = (R_km * length_km) / (Zbase * factor)
    X_line_PU = (X_km * length_km) / (Zbase * factor)
    return complex(R_line_PU, X_line_PU)

# สมมุติข้อมูลเบื้องต้นของหม้อแปลง (คุณสามารถเปลี่ยนตามความเหมาะสม)
Vbase_22kV = 22          # kV
Sbase_22kV = 100         # MVA
Zbase_22kV = Vbase_22kV ** 2 / Sbase_22kV  # ค่า Z base
Ibase_22kV = Sbase_22kV / (cmath.sqrt(3) * Vbase_22kV)

# อิมพีแดนซ์ของหม้อแปลง (pu)
Z1_PU = complex(0.08523, 0.58138)
Z0_PU = complex(0.01769, 0.30910)

# สมมุติข้อมูลสายส่งสำหรับ 10 โหนด (ตัวอย่างนี้ใช้ข้อมูลสมมุติ)
# สำหรับแต่ละ node เรากำหนดความยาวสาย (km), ค่า R/km และ X/km
node_lines = [
    {"node": 1, "length_km": 1.21, "R_km": 0.2106598, "X_km": 0.2985855},
    {"node": 2, "length_km": 0.80, "R_km": 0.2200000, "X_km": 0.3100000},
    {"node": 3, "length_km": 1.00, "R_km": 0.2000000, "X_km": 0.2900000},
    {"node": 4, "length_km": 1.50, "R_km": 0.2300000, "X_km": 0.3200000},
    {"node": 5, "length_km": 0.90, "R_km": 0.2100000, "X_km": 0.3000000},
    {"node": 6, "length_km": 1.10, "R_km": 0.2150000, "X_km": 0.3050000},
    {"node": 7, "length_km": 1.30, "R_km": 0.2250000, "X_km": 0.3150000},
    {"node": 8, "length_km": 0.70, "R_km": 0.2050000, "X_km": 0.2950000},
    {"node": 9, "length_km": 1.40, "R_km": 0.2350000, "X_km": 0.3250000},
    {"node": 10, "length_km": 1.00, "R_km": 0.2206598, "X_km": 0.2985855},
]

# คำนวณกระแสฟอลต์ 3 เฟสสำหรับแต่ละโหนด
# สมมุติว่าแรงดันก่อนฟอลต์เป็น 1 pu และใช้สูตร I_fault = 1 / (Z1_PU + Z_line)
print("Fault Current 3P at each Node (Actual):")
for item in node_lines:
    node = item["node"]
    line_impedance = get_line_parameters(item["length_km"], item["R_km"], item["X_km"], Zbase_22kV)
    total_impedance = Z1_PU + line_impedance
    I_fault_pu = 1 / total_impedance  # คำนวณเป็น pu
    I_fault_actual = abs(I_fault_pu) * Ibase_22kV
    print(f"Node {node}: Fault Current = {I_fault_actual:.2f} A (Total Impedance: {abs(total_impedance):.3f} pu)")
