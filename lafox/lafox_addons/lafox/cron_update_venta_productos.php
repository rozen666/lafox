<?php
###############################################################################
#                                       	
#
#    Code create by: Ing. Luis J. Ortega 
#    Code created to update the percentage of products 
#    sold per month, with respect to the product of the warehouse
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

	// FUNCION QUE PERMITE AGRUPAR LOS DATOS DE UN ARRAY POR UN CAMPO EN ESPECIFICO
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

	function update_reset_ventas( $conexion )
	{	
		// QUERY PARA LA ACTUALIZACIÓN MENSUAL DE PORCENTAJE DE CADA PRODUCTO
		$mes_a = date("m");
		$month = date('m');
		$year = date('Y');
		$u_day = date("d", mktime(0,0,0, $month+1, 0, $year));
		$u_day = date('Y-m-d', mktime(0,0,0, $month, $u_day, $year));
		$day_i = date('Y-m-d', mktime(0,0,0, $month, 1, $year));
		$array_p =array();

		$sql = "UPDATE product_product SET mes_venta='$mes_a',porcentaje_vendido=0, producto_move = 0, producto_vendidos = 0 WHERE mes_venta != '$mes_a' OR mes_venta IS null";
		// $sql = "UPDATE product_product SET mes_venta='$mes_a',porcentaje_vendido=0,state_product='' WHERE mes_venta != '$mes_a'";
		$rs = pg_query( $conexion, $sql );
		// var_dump($rs);

		$sql_stock = "SELECT product_id,id,create_date,name,product_uom_qty FROM stock_move WHERE state = 'done' AND location_dest_id = 12 AND create_date BETWEEN '".$day_i." 00:00:01' AND '".$u_day." 23:59:59' ";

		// echo  $sql_stock;die();
		$rs_stock = pg_query( $conexion, $sql_stock );
		while($row = pg_fetch_row($rs_stock)) {
			$array_p[] = array('producto'=>$row[0],'product_id'=>$row[0],'name'=>$row[3],'cantidad'=>$row[4]);
		}

		return $array_p;

	}

	function update_count_ventas( $conexion )
	{	
		// QUERY PARA LA ACTUALIZACIÓN MENSUAL DE LA VENTA DE UNIDADES POR PRODUCTO
		$mes_a = date("m");
		$month = date('m');
		$year = date('Y');
		$u_day = date("d", mktime(0,0,0, $month+1, 0, $year));
		$u_day = date('Y-m-d', mktime(0,0,0, $month, $u_day, $year));
		$day_i = date('Y-m-d', mktime(0,0,0, $month, 1, $year));
		$array_p =array();

		$sql_sell = "SELECT AL.id,
							AL.create_date,
							AL.product_id,
							AL.name,
							AL.quantity 
					FROM account_invoice 
					INNER JOIN account_invoice_line AL ON account_invoice.id = AL.invoice_id 
					WHERE account_invoice.state in ('paid','open') AND account_invoice.create_date BETWEEN '".$day_i." 00:00:01' AND '".$u_day." 23:59:59' ";

		$rs_sell = pg_query( $conexion, $sql_sell );
		
		while($row = pg_fetch_row($rs_sell)) {
			$array_p[] = array('id'=>$row[0],'fecha'=>$row[1],'product_id'=>$row[2],'producto'=>$row[2],'name'=>$row[3],'cantidad'=>$row[4]);
		}
		
		return $array_p;

	}

	function update_res_parnter_ventas( $conexion )
	{	
		// QUERY PARA LA ACTUALIZACIÓN MENSUAL DE LA VENTA DE UNIDADES POR CLIENTE
		$mes_a = date("m");
		$month = date('m');
		$year = date('Y');
		$u_day = date("d", mktime(0,0,0, $month+1, 0, $year));
		$u_day = date('Y-m-d', mktime(0,0,0, $month, $u_day, $year));
		$day_i = date('Y-m-d', mktime(0,0,0, $month, 1, $year));
		$array_p =array();

		$sql_sell = "SELECT id,
							fecha_venta,
							amount_total,
							partner_id
					FROM account_invoice 
					WHERE state in ('paid','open') AND create_date BETWEEN '".$day_i." 00:00:01' AND '".$u_day." 23:59:59' ORDER BY fecha_venta DESC";

		$rs_sell = pg_query( $conexion, $sql_sell );
		while($row = pg_fetch_row($rs_sell)) {
			$array_p[] = array('id'=>$row[0],'fecha'=>$row[1],'amount_total'=>$row[2],'partner_id'=>$row[3],'producto'=>$row[3]);
		}
		
		return $array_p;

	}

	// FUNCION PARA ACTUALIZAR LA TABLA PRODUCT_PRODUCT
	function Update_Data_DB( $conexion, $groupventa, $y){
		foreach($groupventa as $products){
			$cant = 0;
			$i=0;
			foreach ($products['groupeddata'] as $producto){
				$cant = $cant +$producto['cantidad'];
				$id_p = $producto['product_id'];
			}
			$q = "UPDATE product_product SET $y='$cant' WHERE id = '$id_p' ";
			$rs = pg_query( $conexion, $q );
		}
	}
	
	// FUNCION PARA ACTUALIZAR LA TABLA RES_PARTNER
	function Update_Data_RP_DB( $conexion, $groupventa){
		foreach($groupventa as $products){
			$cant = 0;
			$i=0;
			foreach ($products['groupeddata'] as $producto){
				$cant = $cant +$producto['amount_total'];
				$id_p = $producto['partner_id'];
				$cant_m = $products['groupeddata'][0]['amount_total'] ;
				$canMax= 0;
				if($canMax <= $producto['amount_total'])
				{
					$canMax = $producto['amount_total'];
				}
			}
			$q = "UPDATE res_partner SET promedio_compra_mensual='$cant',ultima_compra_mensual='$cant_m',mayor_compra_mensual ='$canMax' WHERE id = '$id_p'";
			$rs = pg_query( $conexion, $q );
		}
	
	}

	// FUNCION PARA OBTNER LAS VETNAS DEL SALDO PENDIENTE POR CLIENTE
	function update_count_saldo_pend( $conexion )
	{	
		// QUERY PARA LA ACTUALIZACIÓN MENSUAL DE LA VENTA DE UNIDADES POR PRODUCTO

		$sql_sp = "SELECT id,
						  fecha_venta,
						  amount_total,
						  partner_id
				    FROM account_invoice WHERE check_credito = 'True'";

		$rs_sell = pg_query( $conexion, $sql_sp );
		while($row = pg_fetch_row($rs_sell)) {
			$array_p[] = array('id'=>$row[0],'fecha'=>$row[1],'amount'=>$row[2],'partner'=>$row[3],'partner_id'=>$row[3]);
		}
		
		return $array_p;

	}
	
	// FUNCION PARA ACTUALIZAR EL SALDO PENDIENTE POR CLIENTE
	function Update_Data_SP_DB( $conexion, $groupventa){
		foreach($groupventa as $products){
			$cant = 0;
			$i=0;
			foreach ($products['groupeddata'] as $producto){
				$cant = $cant +$producto['amount'];
				$id_p = $producto['partner_id'];
			}
			$q = "UPDATE res_partner SET saldo_pendiente='$cant' WHERE id = '$id_p'";
			$rs = pg_query( $conexion, $q );
		}
	
	}

	// FUNCION PARA ACTUALIZAR EL PORCENTAJE DE VENTA POR PRODUCTO
	function Update_Porcentajes_Venta( $conexion){
		$mes_a = date("m");
		$sql_sp = "SELECT id,producto_move,producto_vendidos,mes_venta
					FROM product_product 
					WHERE producto_move > 0
					AND producto_vendidos > 0 AND
					mes_venta = '$mes_a'";	

		$rs_sell = pg_query( $conexion, $sql_sp );
		while($row = pg_fetch_row($rs_sell)) {
			$porVend = ((float)$row[2] * 100) / (float)$row[1];
			$q = "UPDATE product_product SET porcentaje_vendido='$porVend' WHERE id = '$row[0]'";
			$rs = pg_query( $conexion, $q );
		}
	}


	// CONEXION A LA BD
	$conexion = conectar_PostgreSQL( "odoo", "pos_lafox", "localhost", "LaFox" );

	// SE OBTIENEN LOS DATOS DE LOS MOVIMIENTOS POR MES Y SE ACTUALIZA LA DB
	$objResetventas = update_reset_ventas( $conexion);
	$groupventa = groupArray($objResetventas,'producto');
	$r_sql = Update_Data_DB($conexion, $groupventa, "producto_move");

	// SE OBTIENEN LOS DATOS DE LOS VENTAS POR MES Y SE ACTUALIZA LA DB
	$objSellventas = update_count_ventas( $conexion);
	$groupventa_p = groupArray($objSellventas,'producto');
	$rv_sql = Update_Data_DB($conexion, $groupventa_p, "producto_vendidos");

	//SE OBTIENEN LOS DATOS DE LOS VENTAS POR MES Y SE ACTUALIZA LA DB
	$objPartnervVenta = update_res_parnter_ventas( $conexion);
	$groupventa_part = groupArray($objPartnervVenta,'producto');
	$rsql = Update_Data_RP_DB($conexion, $groupventa_part);

	// SE OBTIENEN LOS DROS POR VENTA PARA ACTUALIZAAR EL SALDO
	$objSaldoPend = update_count_saldo_pend( $conexion);
	$groupSP = groupArray($objSaldoPend,'partner');
	$rsql_sp = Update_Data_SP_DB($conexion, $groupSP);

	// SE ACTULIZAN LOS PORCENTAJES DE VENTA POR MES DE CADA PRODUTO
	$objProduct = Update_Porcentajes_Venta($conexion);

?>
