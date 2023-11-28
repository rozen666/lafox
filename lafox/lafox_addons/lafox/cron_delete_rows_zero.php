<?php
	##############################################################################
	#
	#
	#    Code create by: Ing. Luis J. Ortega and M. Flores
	#    Code created to update the users are active on the system
	#    and desactive users there are on suspended.
	# 
	##############################################################################
	// Con esta línea mostramos los posibles errores:
	ini_set("display_errors", "on");

	
	// Función para conectarse al POSTGRES DE ODOO
	function conectar_PostgreSQL( $usuario, $pass, $host, $bd )
	{
		$conexion = pg_connect( "user=".$usuario." ".
				  		   "password=".$pass." ".
						   "host=".$host." ".
						   "dbname=".$bd
						  ) or die( "Error al conectar: ".pg_last_error() );

		return $conexion;
	}

	function deleteStock_Quant_and_Move( $conexion )
	{	

		$sql = "SELECT * FROM stock_quant WHERE qty = 0";
		$rs = pg_query( $conexion, $sql );
		$row = pg_fetch_all($rs);
		
		if ($row){
			   	
	   	// FUNCION PARA ELIMINAR REGISTROS EN 0 EN STOCK QUANT Y MOVE
			$sqlQ = "DELETE FROM stock_quant WHERE qty = 0";
			// Ejecutar la consulta:
			$rsQ = pg_query( $conexion, $sqlQ );
			if(!$rsQ) {
	      		echo pg_last_error($conexion);
	      		exit;
	   		}
	   		$sqlM = "DELETE FROM stock_move WHERE product_uom_qty = 0";
			// Ejecutar la consulta:
			$res = pg_query( $conexion, $sqlM );
			if(!$res) {
	      		echo pg_last_error($conexion);
	      		exit;
	   		}
	   	}
   	}


	$conexion = conectar_PostgreSQL( "odoo", "pos_lafox", "localhost", "LaFox" );
	$objDelete = deleteStock_Quant_and_Move( $conexion);





