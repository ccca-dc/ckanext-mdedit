  /* Set the value of textarea #{{ id }} to the value of select menu #select-{{ id }}
   * IDs are hard-coded, as this script lives at the same level as the IDs are defined
   */
  mdedit_updateInput(mdedit_select_id){
      console.log("Anja ---------------------- select_id")
      $("#mdedit_select_id").val($("#mdedit_select_id").val());
  }
