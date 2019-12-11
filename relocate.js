<script>
window.onload = function()
{
	str1 = window.location.hash;
	
	if (str1.includes("#"))
	{
		str1 = str1.replace("#", "?");
		window.location = window.location.pathname + str1
	}
}
</script>