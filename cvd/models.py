from django.db import models
from cnf.models import Paciente, ClaseModelo2, UmEdad, GrupoPob, Eps, Muestra, Departamento, Municipio, \
Pais, Tipocontacto, Tipoconglomerado, Evento, Ocupacion, Regimen, ClasiFinicial, Upgd, SemEpidemiologica, \
Funcionario, RedLaboratorios, Muestra, ActividadEconomica, TipoTrabajo, Barrio


from bai.models import Diagnosticos

# Create your models here.

class ClaseContacto(ClaseModelo2):
	descripcion = models.CharField(max_length=80)

	class Meta:
		verbose_name = 'Clase de contacto'

	def __str__(self):
		return "{}".format(self.descripcion)


class AmbitoAtencion(ClaseModelo2):
	descripcion = models.CharField(max_length=80)

	class Meta:
		verbose_name='Ambito de Atención Hospitalaria'

	def __str__(self):
		return "{}".format(self.descripcion)

class ImportSivCvdFile(ClaseModelo2):
	semepidemiologica = models.ForeignKey(SemEpidemiologica, on_delete=models.CASCADE)
	evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
	file_name = models.FileField(upload_to='cvd')
	uploaded =models.DateField(auto_now_add=True)
	activated= models.BooleanField(default=False)

	def save(self):
		#self.uc = instance.request.user
		super(ImportSivCvdFile, self).save()

	def __str__(self):
		return f"Id del Archivo {self.id}"

class Bac(ClaseModelo2):
	POSNEG = (
        ('+', '+'),
        ('-', '-'),
        ('NA', 'No Aplica'),
    )
	SINO = (
        ('SI', 'Si'),
        ('NO', 'No'),
        ('NA', 'No Aplica'),
    )
	
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
	fecharealiza = models.DateField()
	edad=models.IntegerField()
	umedad = models.ForeignKey(UmEdad, on_delete=models.CASCADE)
	grupopob=models.ForeignKey(GrupoPob, on_delete=models.CASCADE)
	riesgopsicosoc = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE, null=True, blank=True)
	tos = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	dificultadrespirar = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	dolorgarganta = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	fiebre = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	sano = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	diabetes = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	enfcardiaca = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	cancer = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	enfrenal = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	trata_corticoides = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	asma_epoc = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	malnutricion = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	otracoomorbilidad = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	temperatura = models.FloatField()
	prueba_olfato = models.CharField(max_length=2, choices=POSNEG, null=True, blank=True)
	sospechoso = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	pruebacovid = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	fichaepidemiologica = models.CharField(max_length=4, null=True, blank=True) 
	resultado = models.CharField(max_length=2, choices=POSNEG, null=True, blank=True)
	observaciones = models.TextField(null=True, blank=True)

	class Meta:
		verbose_name='Busqueda Activa Comunitaria'

	def __str__(self):
		return "{} - {} ".format(fecharealiza, paciente)

class Fichaiec(ClaseModelo2):
	ESTADOIEC = (
        ('ACT', 'Activo'),
        ('CUR', 'Curado'),
        ('FAL', 'Fallecido'),
    )
	POSNEG = (
        ('+', '+'),
        ('-', '-'),
        ('NA', 'No Aplica'),
    )
	SINO = (
        ('SI', 'Si'),
        ('NO', 'No'),
        ('NA', 'No Aplica'),
    )
	fecha=models.DateField()
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
	actividadeconomica = models.ForeignKey(ActividadEconomica, on_delete=models.CASCADE, null=True, blank=True)
	tipotrabajo = models.ForeignKey(TipoTrabajo, on_delete=models.CASCADE, blank=True, null=True)
	fecinisintomas = models.DateField(null=True, blank=True)
	desplazamientos = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	contact_pac = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	lugarcontact = models.CharField(max_length=150, blank=True, null=True)
	antinflamatorios = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	fiebre = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	tos = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	dificultadrespirar = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	taquipnea = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	dolorgarganta = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	escalofrios = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	nauseas = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	vomito = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	dolor_torax = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	mialgia = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	diarrea = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	dolor_abdominal = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	dolor_cabeza = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	malestar_general = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	otro = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	cualotro = models.CharField(max_length=150, null=True, blank=True) 
	asma=models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	epoc = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	trastorno_neuro = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	inmunosupresion = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	enfrenal = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	enfcardiaca = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	enfhematologica = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	diabetes = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	obesidad = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	enfhepatica = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	embarazo = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	semgestacion = models.FloatField(null=True, blank=True) 
	tabaquismo = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	alcoholismo = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	trastorno_reumatologico = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	fechaprimuestra=models.DateField(null=True, blank=True)
	muestra = models.ForeignKey(Muestra, on_delete=models.CASCADE, null=True, blank=True)
	cualotramuestra = models.CharField(max_length=150, null=True, blank=True)
	resfilarray=models.CharField(max_length=2, choices=POSNEG, null=True, blank=True)
	respcr=models.CharField(max_length=2, choices=POSNEG, null=True, blank=True)
	fechareslab = models.DateField(null=True, blank=True)
	anamnesis = models.TextField(null=True, blank=True)
	nomapentrevistador = models.CharField(max_length=150, null=True, blank=True)
	telentrevistador = models.CharField(max_length=30, null=True, blank=True)
	departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
	municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)
	estadoiec = models.CharField(max_length=3, default='ACT', choices=ESTADOIEC) 
	fechaegreso = models.DateField(null=True, blank=True)
	ambitoatencion = models.ForeignKey(AmbitoAtencion, on_delete=models.CASCADE, default=1)
	

	
	def __str__(self):
		return "{} - {}".format(self.fecha, self.paciente)

	def save(self):
		print(self)
		super(Fichaiec, self).save()

	class Meta:
		verbose_name = "Fichas IEC"
		ordering=['fecha','paciente']


class ContactosIec(ClaseModelo2):
	POSNEG = (
        ('+', '+'),
        ('-', '-'),
        ('NA', 'No Aplica'),
    )
	SINO = (
        ('SI', 'Si'),
        ('NO', 'No'),
        ('NA', 'No Aplica'),
    )

	fichaiec = models.ForeignKey(Fichaiec, on_delete=models.CASCADE)
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
	edad = models.IntegerField(null=True, blank=True)
	umedad = models.ForeignKey(UmEdad, on_delete=models.CASCADE, null=True, blank=True)
	clasecontacto = models.ForeignKey(ClaseContacto, on_delete=models.CASCADE)
	fechaposexpo=models.DateField(null=True, blank=True)	
	institucionsalud = models.CharField(max_length=150, null=True, blank=True)
	sintomatico = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	fechainisintomas = models.DateField(null=True, blank= True)
	hospitalizado = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	fechamuestra = models.DateField(null=True, blank=True)
	resultmxcovid = models.CharField(max_length=2, choices=POSNEG, null=True, blank=True)

	class Meta:
		verbose_name='Contactos'

	def __str__(self):
		return "Caso Indice: {} - Contacto: {}".format(self.fichaiec, self.paciente)

class DesplazaContacto(ClaseModelo2):
	contactosiec = models.ForeignKey(ContactosIec, on_delete=models.CASCADE)
	pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
	departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
	ciudad = models.CharField(max_length=100)

	class Meta:
		verbose_name='Desplazamientos de los contactos'

class SegContacto(ClaseModelo2):
	SINO = (
        ('SI', 'Si'),
        ('NO', 'No'),
        ('NA', 'No Aplica'),
    )
	contactosiec = models.ForeignKey(ContactosIec, on_delete=models.CASCADE)
	fecha = models.DateTimeField()
	sintomatico =models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	tos =models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	fiebre =models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	odinofagia =models.CharField(max_length=2, choices=SINO, null=True, blank=True)	
	difrespirar=models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	adinamia =models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	hospitalizado =models.CharField(max_length=2, choices=SINO, null=True, blank=True)

	class Meta:
		verbose_name='Seguimientos a Contactos'
		ordering=['fecha']


class FileFichaIec(ClaseModelo2):		
	fichaiec = models.ForeignKey(Fichaiec, on_delete=models.CASCADE)
	descripcion = models.CharField(max_length=200)
	archivo = models.FileField(upload_to='cvd', null=True, blank=True)

class Antecedenteviaje(ClaseModelo2):
	fichaiec = models.ForeignKey(Fichaiec, on_delete=models.CASCADE)
	pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
	ciudad = models.CharField(max_length=100)
	fechaini = models.DateField()
	fechafin = models.DateField()

	class Meta:
		ordering=['fechaini']

class EstadoAfectacion(ClaseModelo2):
	descripcion=models.CharField(max_length=80)

	class Meta:
		verbose_name='Estado de afectación'

	def __str__(self):
		return "{}".format(self.descripcion)

class AntecHospitalizacion(ClaseModelo2):
	fichaiec = models.ForeignKey(Fichaiec, on_delete=models.CASCADE)
	fechaconsulta = models.DateField()
	institucionsalud = models.CharField(max_length=150)
	observacion = models.TextField(blank=True, null=True)

	class Meta:
		ordering=['fechaconsulta']

class SegFichaIec(ClaseModelo2):
	RESULTADOPCVD=(
		('POS','Positivo'),
		('NEG','Negativo'),
		('PEN','Pendiente'),	
		('NRE','No Realizada'),	
		)
	SINO = (
        ('SI', 'Si'),
        ('NO', 'No'),
        ('NA', 'No Aplica'),
    )
	fichaiec=models.ForeignKey(Fichaiec, on_delete=models.CASCADE)
	fecha=models.DateField()
	resprapida=models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	fiebremasdosdias = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	pechosuena=models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	somnolencia =models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	ataqueconvulsion=models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	decaimiento=models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	deteriorogeneral=models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	dificultadrespirar=models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	hallazgo=models.TextField()
	tipocontacto = models.ForeignKey(Tipocontacto, on_delete=models.CASCADE)
	pendiente = models.CharField(max_length=2, choices=SINO, null=True, blank=True) 
	descpendiente = models.TextField(null=True, blank=True)
	fechaprog=models.DateField(null=True, blank=True)	
	resultadopcvd = models.CharField(max_length=3, default='PEN', choices=RESULTADOPCVD) 
	fechaultprueba = models.DateField(null=True, blank= True)	
	nombreinforma = models.CharField(max_length=100)
	cargoactividadinfo=models.CharField(max_length=100, null=True, blank=True)
	telfijoinfo = models.CharField(max_length=30, null=True, blank=True)
	celularinfo = models.CharField(max_length=30, null=True, blank=True)
	emailinfo = models.CharField(max_length=30, null=True, blank=True)
	estadoafectacion = models.ForeignKey(EstadoAfectacion, on_delete=models.CASCADE, null=True, blank=True)
	ambitoatencion = models.ForeignKey(AmbitoAtencion, on_delete=models.CASCADE, null=True, blank=True, default=1) 


	def __str__(self):
		return "{} : {}".format(self.fecha, self.hallazgo)

	class Meta:
		verbose_name = "Seguimiento Fichas IEC"
		ordering=['fichaiec','fecha']

class Conglomerado(ClaseModelo2):
	SINO = (
        ('SI', 'Si'),
        ('NO', 'No'),
        ('NA', 'No Aplica'),
    )
	tipoconglomerado=models.ForeignKey(Tipoconglomerado, on_delete=models.CASCADE)
	descripcion=models.CharField(max_length=150)
	nomreplegal=models.CharField(max_length=100, null=True, blank=True)
	telcontacto = models.CharField(max_length=30, null=True, blank=True)	
	direccion=models.CharField(max_length=100, null=True, blank=True)		
	lat = models.CharField(max_length=20, blank = True, null=True, default='SD')
	lon = models.CharField(max_length=20, blank=True, null=True, default='SD')
	
	def __str__(self):
		return "{}".format(self.descripcion)

	class Meta:
		verbose_name = "Config. Puntos Calientes - Conglomerados"
		ordering=['descripcion']

class ConfigConglomerado(ClaseModelo2):
	CONTROLADO = (
        ('CONTROLADO', 'CONTROLADO'),
        ('EN PROCESO', 'EN PROCESO'),  
        ('DESCONTROLADO', 'DESCONTROLADO'),       
    )
	ESTADO = (
        ('ABIERTO', 'ABIERTO'),
        ('CERRADO', 'CERRADO'),        
    )
	conglomerado = models.ForeignKey(Conglomerado, on_delete=models.CASCADE)
	consecutivo = models.IntegerField()	
	descripcion = models.TextField(null=True, blank=True)
	barrio=models.ForeignKey(Barrio, on_delete=models.CASCADE, null=True, blank=True)
	descmedidasinstitucion = models.TextField(null=True, blank=True)
	descmeorgasalud = models.TextField(null=True, blank=True)
	nrocasospos = models.IntegerField(null=True, blank=True)
	nrocasosneg = models.IntegerField(null=True, blank=True)
	nrocasospendiente = models.IntegerField(null=True, blank=True)	
	totalperaislados = models.IntegerField(null=True, blank=True)
	fuente = models.CharField(max_length=100, null=True, blank=True)
	causacontagio = models.CharField(max_length=100, null=True, blank=True)
	nrocasosrelacionados = models.IntegerField(null=True, blank=True)
	estadoconglomerado = models.CharField(max_length=20, choices=ESTADO, null=True, blank=True) 
	fichaiec = models.ManyToManyField(Fichaiec, verbose_name='Usuarios Conglomerado') 
	medidascorrectivas = models.TextField(null=True, blank=True)
	controlado = models.CharField(max_length=20, choices=CONTROLADO, null=True, blank=True) 

	class Meta:
		verbose_name='Conglomerado'
		ordering=['conglomerado','consecutivo']

	def __str__(self):
		return "{} : No. {}".format(self.conglomerado,self.nrocasospos)


class Notif_covid(ClaseModelo2):
	HALLAZGORX = (
        ('1', 'Infiltrado alveolar o neumonía'),
        ('2', 'Infiltrados intersticiales'),
        ('3', 'Ninguno'),
    )
	CONDICFINAL = (
        ('1', 'Vivo'),
        ('2', 'Muerto'),
        ('0', 'Sin Dato'),
    )
	SINO = (
        ('1', 'Si'),
        ('2', 'No'),
    )
	paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE)
	evento=models.ForeignKey(Evento, on_delete=models.CASCADE)
	fec_not = models.DateField()
	semana = models.IntegerField()
	anio = models.IntegerField()
	cod_pre = models.CharField(max_length=20)
	cod_sub = models.CharField(max_length=2)
	edad = models.IntegerField()
	umedad = models.ForeignKey(UmEdad, on_delete=models.CASCADE, null=True, blank=True)
	ocupacion = models.ForeignKey(Ocupacion, on_delete=models.CASCADE, null=True, blank=True)
	regimen = models.ForeignKey(Regimen, on_delete=models.CASCADE)
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE, null=True, blank=True)
	estrato = models.IntegerField(null=True, blank=True)
	gp_discapa = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_desplaz = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_migrant = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_carcela = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_gestan = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	sem_ges = models.IntegerField(null=True, blank=True) 
	gp_indigen = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_pobicbf = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_mad_com = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_desmovi = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_psiquia = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_vic_vio = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_otros = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	Departamentor = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
	municipior = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)
	fec_con = models.DateField(null=True, blank=True)
	ini_sin = models.DateField(null=True, blank=True)
	clasiFinicial = models.ForeignKey(ClasiFinicial, on_delete=models.CASCADE, null=True, blank=True)
	pac_hos = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	fec_hos = models.DateField(null=True, blank=True)
	con_fin = models.CharField(max_length=1, choices=CONDICFINAL, null=True, blank=True)
	fed_def =  models.DateField(null=True, blank=True)
	cer_def = models.CharField(max_length=30, null=True, blank=True)
	cbmte = models.CharField(max_length=10, null=True, blank=True)
	dxmuerte = models.ForeignKey(Diagnosticos, on_delete=models.CASCADE, null=True, blank=True)
	telefono = models.CharField(max_length=30, null=True, blank=True)
	nit_upgd = models.CharField(max_length=30, null=True, blank=True)
	upgd = models.ForeignKey(Upgd, on_delete=models.CASCADE, null=True, blank=True)
	trab_salud = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	deter_clin = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	asoc_brote = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	viaje = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	municipioviajo = models.IntegerField(null=True, blank=True)#municpio al que viajó 
	codpais_pr = models.ForeignKey(Pais, on_delete=models.CASCADE, null = True, blank=True)	
	con_con = models.CharField(max_length=1, choices=SINO, null=True, blank=True) #Tuvo contacto ultimos 14 dias
	con_est = models.CharField(max_length=1, choices=SINO, null=True, blank=True) #contacto estrecho	
	tos = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	fiebre = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	odinofagia	= models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	dif_res	= models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	adinamia = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	vac_ei = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	dos_ei = models.IntegerField(null=True, blank=True) #nro de dosis de Influenza
	asma = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	epoc = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	diabetes = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	vih = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	enf_card = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	cancer = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	desnutricion = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	obesidad = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	ins_renal = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	otr_medinm =models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	fumador = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	tuberculos = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	otros_dc = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	cual_ot_dc = models.CharField(max_length=150, choices=SINO, null=True, blank=True) 
	hallaz_rad = models.CharField(max_length=1, choices=HALLAZGORX, null=True, blank=True) 
	uso_antib = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	uso_antiv = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	fec_antiv = models.DateField(null=True, blank=True)
	serv_hosp = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	fec_inguci = models.DateField(null=True, blank=True)
	der_ple = models.CharField(max_length=1, choices=SINO, null=True, blank=True) #derrame pleural
	der_per = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	miocarditi = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	septicemia = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	falla_resp = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	otros_sint = models.CharField(max_length=1, choices=SINO, null=True, blank=True) #Otros sintomas
	dol_gar = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	rinorrea = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	conjuntivi = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	cefalea = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	diarrea = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	rx_torax = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	fec_tom_ra = models.DateField(null=True, blank=True)
	fec_atib =  models.DateField(null=True, blank=True)
	otros_cual = models.CharField(max_length=150, blank=True, null=True)
	dx_ini = models.CharField(max_length=10, null=True, blank=True)
	dx_egr =  models.CharField(max_length=10, null=True, blank=True)
	semana_ges = models.IntegerField(null=True, blank=True)

	class Meta:
		verbose_name_plural="Notificación Dengue - 210"
	def __str__(self):
		return "{} {} {} - {}".format(self.fec_not, self.semana ,self.evento.descripcion, self.paciente)

class Segnotifcovid(ClaseModelo2):
	SINO = (
        ('1', 'Si'),
        ('2', 'No'),
    )
	notifcovid = models.ForeignKey(Notif_covid, on_delete=models.CASCADE)
	fecha = models.DateField()
	hallazgo = models.TextField()
	proxseg = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	fecproxseg = models.DateField(null=True, blank=True)
	fileseg = models.FileField(upload_to='cvd', null=True, blank=True)

class NotifPaConglomerado(ClaseModelo2):
	RESULTADO = (
        ('POS', 'Positivo'),
        ('NEG', 'Negativo'),
    )	
	conglomerado = models.ForeignKey(Conglomerado, on_delete=models.CASCADE)
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
	edad = models.IntegerField(null=True, blank=True)
	municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE)
	fecinisintomas = models.DateField()
	fechatomamuestra = models.DateField(null=True, blank=True)
	resultado = models.CharField(max_length=3, choices=RESULTADO, null=True, blank=True)
	descripcion = models.TextField(null=True, blank=True)
	observacion = models.TextField(null=True, blank=True)

	class Meta:
		verbose_name='FICHA DE NOTIFICACION DE CASOS - CONGLOMERADO'

	def __str__(self):
		return "{} : {}".format(self.paciente, self.conglomerado)


class ContactoAislado(ClaseModelo2):
	SINOPRUEBA = (
        ('SI', 'Si'),
        ('NO', 'No reúne criterios'),
    )
	SINO = (
   	    ('SI', 'Si'),
        ('NO', 'No'),
    )
	RESULTADO = (
        ('POS', 'Positivo'),
        ('NEG', 'Negativo'),
    )
	notifPaConglomerado = models.ForeignKey(NotifPaConglomerado, on_delete=models.CASCADE)	
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
	edad = models.IntegerField(null=True, blank=True)
	cargo = models.CharField(max_length=100, null=True, blank=True)
	municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE)
	feciniaislamiento = models.DateField()
	fechafinaislamiento = models.DateField(null=True, blank=True)
	valmedicagral = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	motivo = models.TextField(null=True, blank=True)
	diasaislamiento = models.IntegerField(default=14, null=True, blank=True)
	aislaconincapacidad = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	requiereprueba = models.CharField(max_length=2, choices=SINOPRUEBA, null=True, blank=True)
	fechatomamuestra = models.DateField(null=True, blank=True)
	resultado = models.CharField(max_length=3, choices=RESULTADO, null=True, blank=True)
	descripcion = models.TextField(null=True, blank=True)

	class Meta:
		verbose_name='Contactos de conglomerados Aislados'

	def __str__(self):
		return "{} - Contacto de: {}".format(self.paciente, self.notifPaConglomerado)

class SegContactoAislado(ClaseModelo2):
	SINO = (
        ('SI', 'Si'),
        ('NO', 'No'),
    )
    
	contactoaislado = models.ForeignKey(ContactoAislado, on_delete=models.CASCADE)
	fecha=models.DateField()
	sintomas = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	tos = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	Fiebre = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	odinofagia = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	dificultadrespirar  = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	fatiga  = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	hospitalizado  = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	observacion = models.TextField(null=True, blank=True)
	funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, null=True, blank=True)

	class Meta:
		ordering=["fecha"]










	























	



