<?php
###############################################################################
#                                       	
#
#    Code create by: Ing. Luis J. Ortega 
#    Code created to update the average monthly sales for each product 
#     	without considering the sells lossed
#
##############################################################################
	// Con esta línea mostramos los posibles errores:
	ini_set("display_errors", "on");

	// ----------------------------------------------
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

	function get_ventas_productos( $conexion )
	{	
		// QUERY PARA OBTENER LAS VENTAS DE LOS PRODUCTOS QUE ESTEN PAGADAS O ABIERTAS
		$sql = "SELECT nomenclatura,account_invoice_line.quantity,product_product.id,date_part('month',account_invoice.fecha_venta) 
				FROM account_invoice_line 
				INNER JOIN account_invoice ON account_invoice_line.invoice_id = account_invoice.id 
				INNER JOIN product_product ON account_invoice_line.product_id = product_product.id 

				WHERE  (date_part('year',account_invoice.fecha_venta) = extract(year from current_timestamp)) and(account_invoice.state = 'open' or account_invoice.state = 'paid')";
		$rs = pg_query( $conexion, $sql );
		
		while($row = pg_fetch_row($rs)) {
			$array_p[] = array('nomenclatura'=>$row[0],'cantidad'=>$row[1],'product_id'=>$row[2],'mes'=>$row[3],'group_id'=>$row[2]);
		}

		return $array_p;

	}

	function groupArray($array,$groupkey)
	{
		 if (count($array)>0)
		 {
		        $keys = array_keys($array[0]);
		        $removekey = array_search($groupkey, $keys);            
		        if ($removekey===false)
		                return array("Clave \"$groupkey\" no existe");
		        else
		                unset($keys[$removekey]);
		        $groupcriteria = array();
		        $return=array();
		        foreach($array as $value)
		        {
		                $item=null;
		                foreach ($keys as $key)
		                {
		                        $item[$key] = $value[$key];
		                }
		                $busca = array_search($value[$groupkey], $groupcriteria);
		                if ($busca === false)
		                {
		                        $groupcriteria[]=$value[$groupkey];
		                        $return[]=array($groupkey=>$value[$groupkey],'groupeddata'=>array());
		                        $busca=count($return)-1;
		                }
		                $return[$busca]['groupeddata'][]=$item;
		        }
		        return $return;
		 }
		 else
		        return array();
	}

	function Update_Data_DB( $conexion, $groupventa, $y){
		foreach($groupventa as $products){
			$cant = 0;
			$i=0;
			foreach ($products['groupeddata'] as $producto){
				$cant = $cant +$producto['cantidad'];
				$id_p = $producto['product_id'];
			}
			$cantidad = $cant / date('m');;
			$q = "UPDATE product_product SET $y='$cantidad' WHERE id = '$id_p' ";
			$rs = pg_query( $conexion, $q );
		}
	}


    // LLAMADO DE LAS FUNCIONES
	$conexion = conectar_PostgreSQL( "odoo", "pos_lafox", "localhost", "LaFox" );
	$groupventa = get_ventas_productos($conexion);
	$grouporpventa = groupArray($groupventa,'group_id');

	$y = "promedio_mensual";
	$r_sql = Update_Data_DB($conexion, $grouporpventa, $y);

	
	// var_dump($grouporpventa);
	// var_dump($grouporpventa);
	// echo "***************************************";
	// var_dump($grouporgmes);
	// var_dump($r_sql);


