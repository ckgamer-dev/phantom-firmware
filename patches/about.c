#include <furi.h>
#include <gui/gui.h>
#include <gui/view_holder.h>
#include <gui/modules/empty_screen.h>
#include <dialogs/dialogs.h>
#include <assets_icons.h>
#include <furi_hal_version.h>
#include <furi_hal_region.h>
#include <furi_hal_bt.h>
#include <furi_hal_info.h>
typedef DialogMessageButton (*AboutDialogScreen)(DialogsApp* d, DialogMessage* m);
static DialogMessageButton s1(DialogsApp* d, DialogMessage* m) {
    dialog_message_set_header(m,"PHANTOM Firmware",0,0,AlignLeft,AlignTop);
    dialog_message_set_text(m,"Ghost in the Machine\nVersion: v0.1.0-alpha\n\nCustom Flipper firmware\nFor research only.",0,13,AlignLeft,AlignTop);
    DialogMessageButton r=dialog_message_show(d,m);
    dialog_message_set_header(m,NULL,0,0,AlignLeft,AlignTop);
    dialog_message_set_text(m,NULL,0,0,AlignLeft,AlignTop); return r;
}
static DialogMessageButton s2(DialogsApp* d, DialogMessage* m) {
    dialog_message_set_header(m,"PHANTOM Features",0,0,AlignLeft,AlignTop);
    dialog_message_set_text(m,"Sub-GHz: 300-928 MHz\nNFC: MIFARE+Dict attack\nIR: Learn + Fuzzer\nBadUSB: DuckyScript\nGPIO: Script engine",0,13,AlignLeft,AlignTop);
    DialogMessageButton r=dialog_message_show(d,m);
    dialog_message_set_header(m,NULL,0,0,AlignLeft,AlignTop);
    dialog_message_set_text(m,NULL,0,0,AlignLeft,AlignTop); return r;
}
static DialogMessageButton s3(DialogsApp* d, DialogMessage* m) {
    dialog_message_set_header(m,"Legal Notice",0,0,AlignLeft,AlignTop);
    dialog_message_set_text(m,"Use ONLY on devices\nyou own or have\nwritten permission.\nObey local RF laws.",0,13,AlignLeft,AlignTop);
    DialogMessageButton r=dialog_message_show(d,m);
    dialog_message_set_header(m,NULL,0,0,AlignLeft,AlignTop);
    dialog_message_set_text(m,NULL,0,0,AlignLeft,AlignTop); return r;
}
static DialogMessageButton s4(DialogsApp* d, DialogMessage* m) {
    FuriString* b=furi_string_alloc();
    const char* n=furi_hal_version_get_name_ptr();
    furi_string_cat_printf(b,"%d.F%dB%dC%d %s %s\nSerial:\n",
        furi_hal_version_get_hw_version(),furi_hal_version_get_hw_target(),
        furi_hal_version_get_hw_body(),furi_hal_version_get_hw_connect(),
        furi_hal_version_get_hw_region_name_otp(),n?n:"Unknown");
    const uint8_t* uid=furi_hal_version_uid();
    for(size_t i=0;i<furi_hal_version_uid_size();i++)
        furi_string_cat_printf(b,"%02X",uid[i]);
    dialog_message_set_header(m,"Hardware Info:",0,0,AlignLeft,AlignTop);
    dialog_message_set_text(m,furi_string_get_cstr(b),0,13,AlignLeft,AlignTop);
    DialogMessageButton r=dialog_message_show(d,m);
    dialog_message_set_text(m,NULL,0,0,AlignLeft,AlignTop);
    dialog_message_set_header(m,NULL,0,0,AlignLeft,AlignTop);
    furi_string_free(b); return r;
}
static DialogMessageButton s5(DialogsApp* d, DialogMessage* m) {
    FuriString* b=furi_string_alloc();
    const Version* v=furi_hal_version_get_firmware_version();
    const BleGlueC2Info* c2=ble_glue_get_c2_info();
    if(!v) furi_string_cat_printf(b,"No info\n");
    else { uint16_t ma,mi; furi_hal_info_get_api_version(&ma,&mi);
        furi_string_cat_printf(b,"%s [%s]\n%s%s [%d.%d] %s\n[%d] %s",
            version_get_version(v),version_get_builddate(v),
            version_get_dirty_flag(v)?"[!] ":"",version_get_githash(v),
            ma,mi,c2?c2->StackTypeString:"none",
            version_get_target(v),version_get_gitbranch(v)); }
    dialog_message_set_header(m,"PHANTOM FW Version:",0,0,AlignLeft,AlignTop);
    dialog_message_set_text(m,furi_string_get_cstr(b),0,13,AlignLeft,AlignTop);
    DialogMessageButton r=dialog_message_show(d,m);
    dialog_message_set_text(m,NULL,0,0,AlignLeft,AlignTop);
    dialog_message_set_header(m,NULL,0,0,AlignLeft,AlignTop);
    furi_string_free(b); return r;
}
const AboutDialogScreen about_screens[]={s1,s2,s3,s4,s5};
int32_t about_settings_app(void* p) {
    UNUSED(p);
    DialogsApp* dialogs=furi_record_open(RECORD_DIALOGS);
    DialogMessage* message=dialog_message_alloc();
    Gui* gui=furi_record_open(RECORD_GUI);
    ViewHolder* vh=view_holder_alloc();
    EmptyScreen* es=empty_screen_alloc();
    size_t idx=0; DialogMessageButton res;
    view_holder_attach_to_gui(vh,gui);
    view_holder_set_view(vh,empty_screen_get_view(es));
    while(1){
        if(idx>=COUNT_OF(about_screens)-1) dialog_message_set_buttons(message,"Back",NULL,NULL);
        else if(idx==0) dialog_message_set_buttons(message,NULL,NULL,"Next");
        else dialog_message_set_buttons(message,"Back",NULL,"Next");
        res=about_screens[idx](dialogs,message);
        if(res==DialogMessageButtonLeft){if(idx<=0)break;else idx--;}
        else if(res==DialogMessageButtonRight){if(idx<COUNT_OF(about_screens)-1)idx++;}
        else break;
    }
    dialog_message_free(message); furi_record_close(RECORD_DIALOGS);
    view_holder_set_view(vh,NULL); view_holder_free(vh);
    empty_screen_free(es); furi_record_close(RECORD_GUI);
    return 0;
}
