from django.shortcuts import render
from django.http import HttpResponse
from .models import Equipment
from django.templatetags.static import static
from .fault_analysis import FaultAnalysis, analyze_nodes_faults

# Create your views here.

def index(request):
    return render(request,"index.html")

def about(request):
    return HttpResponse("<h1>ความสำคัญ ของ Line-Coordination</h1>")

def Title_Box(request):
    return HttpResponse("<h1>Title_Box</h1>")

def diagram_view(request):
    equipments = Equipment.objects.all()
    context = {
         'equipments': equipments,
         'ExternalGrid_url': static('svg/External_grid.svg'),
         'Recloser_url': static('svg/Recloser.svg'),
         'Fuse_url': static('svg/Fuse.svg'),
         'Line_url': static('svg/Line.svg'),
         
    }
    return render(request, 'SCAnalysis.html', context)

def custom_404(request, exception):
    """
    Custom 404 error view
    """
    return render(request, '404.html', status=404)

def custom_500(request):
    """
    Custom 500 error view
    """
    return render(request, '500.html', status=500)


def fault_analysis_view(request):
    """
    View สำหรับแสดงผลการวิเคราะห์กระแสฟอลต์ของแต่ละโหนด
    """
    # ตัวอย่างข้อมูลสายส่งของแต่ละ node
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
    # สร้างอินสแตนซ์ของ FaultAnalysis
    fa = FaultAnalysis(Vbase_kV=22, Sbase_MVA=100)
    # วิเคราะห์ค่ากระแสฟอลต์ที่โหนด
    node_results = analyze_nodes_faults(node_lines, fa)
    context = {
        'node_results': node_results,
    }
    return render(request, 'fault_analysis.html', context)

