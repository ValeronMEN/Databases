<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:template match="/"> 
<html lang="ru">
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
<title>Price table</title>
</head>
<body>
<table>
<tr>
<th>Price</th>
<th>Description</th>
<th>Image</th>
</tr>
<tr>
<xsl:apply-templates select="*"/>
</tr>
</table>
</body>
</html>
</xsl:template>

<xsl:template match="product">
<tr>
<td><xsl:value-of select="price/text()"/></td>
<td><xsl:value-of select="desc/text()"/></td>
<td><xsl:value-of select="img/text()"/></td>
</tr>
</xsl:template>
</xsl:stylesheet>

