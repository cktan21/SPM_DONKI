<!-- This page is just to make the login the default page.
 
If you go to localhost:3000/, it would redirect to localhost:3000/auth/login -->

<script setup>
import { navigateTo } from "#app";

navigateTo("/auth/login");
</script>
