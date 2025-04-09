import cmath

def get_line_parameters(length_km, R_km, X_km, Zbase, factor=1.1):
    """
    คำนวณอิมพีแดนซ์ของสายส่งในหน่วย per unit (pu)
    """
    R_line_PU = (R_km * length_km) / (Zbase * factor)
    X_line_PU = (X_km * length_km) / (Zbase * factor)
    return complex(R_line_PU, X_line_PU)

class FaultAnalysis:
    """
    คลาสสำหรับคำนวณกระแสฟอลต์ในระบบไฟฟ้า
    """
    def __init__(self, Vbase_kV=22, Sbase_MVA=100):
        self.Vbase = Vbase_kV
        self.Sbase = Sbase_MVA
        # คำนวณค่า Z base (ohm)
        self.Zbase = (self.Vbase ** 2) / self.Sbase  
        # คำนวณค่า I base (A)
        self.Ibase = self.Sbase / (cmath.sqrt(3) * self.Vbase)
        # กำหนดอิมพีแดนซ์ของหม้อแปลง (pu)
        self.Z1 = complex(0.08523, 0.58138)   # positive sequence
        self.Z0 = complex(0.01769, 0.30910)   # zero sequence

    def compute_node_fault_current(self, line_impedance_pu):
        """
        คำนวณกระแสฟอลต์ 3 เฟส (Actual) ที่โหนด โดยรวมอิมพีแดนซ์ของหม้อแปลงและสายส่ง
        """
        Z_total = self.Z1 + line_impedance_pu
        if Z_total == 0:
            raise ValueError("Total impedance cannot be zero.")
        I_fault_pu = 1 / Z_total
        return abs(I_fault_pu) * self.Ibase, abs(Z_total)

def analyze_nodes_faults(node_lines, fault_analysis_instance):
    """
    วิเคราะห์ค่ากระแสฟอลต์ที่โหนดจากข้อมูลสายส่ง (node_lines)
    """
    results = []
    for item in node_lines:
        node = item["node"]
        line_impedance = get_line_parameters(
            item["length_km"],
            item["R_km"],
            item["X_km"],
            fault_analysis_instance.Zbase
        )
        I_fault, Z_total = fault_analysis_instance.compute_node_fault_current(line_impedance)
        results.append({
            "node": node,
            "fault_current_actual": I_fault,
            "total_impedance_pu": Z_total
        })
    return results