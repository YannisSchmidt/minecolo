package com.minecolonies.api.client.render.modeltype;

import com.minecolonies.api.entity.citizen.AbstractEntityCitizen;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.Pose;
import org.jetbrains.annotations.NotNull;

/**
 * Citizen model.
 */
public class CitizenModel<T extends AbstractEntityCitizen> extends HumanoidModel<AbstractEntityCitizen>
{
    /**
     * Working render meta.
     */
    private static final String RENDER_META_WORKING = "working";

    public static boolean isItApril1st = false;

    /**
     * Inflation (in 1/16 of a block, per axis x / y / z of a cube) applied to every band of the bust of the adult
     * female citizen models. The Blockbench exports put a single flat 8x3x3 cube here with
     * {@code new CubeDeformation(0.0F)}; the models in this fork build the chest out of eight thin bands (two
     * rounded lobes of four bands, see {@link com.minecolonies.core.client.model.FemaleCitizenModel}) and all of
     * them use this constant, so this single line sets the bust size of every female citizen. The x axis stays
     * small so the arms do not clip into the shape. The four bands of a lobe are 1.05 tall and step by 1.0 (they
     * overlap a little so no two faces are ever coplanar), which spans 4.05 px instead of the original 3 px, so y
     * should stay at or below ~1.0 before the top band starts to poke out of the collar.
     * {@code new CubeDeformation(0.0F)} shrinks the bust down to the untouched shape and size of the bands.
     */
    public static final CubeDeformation BREAST_DEFORMATION = new CubeDeformation(0.35F, 0.6F, 1.25F);

    public CitizenModel(final ModelPart part)
    {
        super(part, RenderType::entityCutoutNoCull);
    }

    @Override
    public void setupAnim(@NotNull final AbstractEntityCitizen citizen, float f1, float f2, float f3, float f4, float f5)
    {
        super.setupAnim(citizen, f1, f2, f3, f4, f5);
        if (body.xRot == 0)
        {
            body.xRot = getActualRotation(citizen);
        }

        if (head.xRot == 0)
        {
            head.xRot = getActualRotation(citizen);
        }

        if (citizen.getCitizenDataView() != null && citizen.getCitizenDataView().getCustomTextureUUID() != null)
        {
            head.visible = false;
            hat.visible = false;
        }
        else
        {
            head.visible = true;
            hat.visible = true;
        }

        if (isItApril1st)
        {
            switch (citizen.getCivilianID() % 7)
            {
                case 0:
                    leftArm.visible = false;
                    break;
                case 1:
                    rightArm.visible = false;
                    break;
                case 2:
                    body.visible = false;
                    break;
                case 3:
                    head.visible = false;
                    break;
                case 4:
                    hat.visible = false;
                    break;
                case 5:
                    leftLeg.visible = false;
                    break;
                case 6:
                    rightLeg.visible = false;
                    break;
            }
        }
    }

    public static LayerDefinition createMesh()
    {
        MeshDefinition meshdefinition = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        return LayerDefinition.create(meshdefinition, 64, 32);
    }

    /**
     * Override to change body rotation.
     *
     * @return the rotation.
     */
    public float getActualRotation(@NotNull final AbstractEntityCitizen entity)
    {
        return 0;
    }

    /**
     * Check if the citizen is supposed to be working.
     * @param citizen the citizen entity to check.
     * @return true if so.
     */
    public boolean isWorking(final AbstractEntityCitizen citizen)
    {
        return citizen.getRenderMetadata().contains(RENDER_META_WORKING);
    }

    /**
     * Check if the hat should be displayed.
     * @param citizen the citizen entity to check.
     * @return true if so.
     */
    public boolean displayHat(final AbstractEntityCitizen citizen)
    {
        if (citizen.getPose() == Pose.SLEEPING || !citizen.getItemBySlot(EquipmentSlot.HEAD).isEmpty())
        {
            return false;
        }
        return citizen.getCitizenDataView() == null || (citizen.getCitizenDataView().getDisplayArmor(EquipmentSlot.HEAD).isEmpty() && citizen.getCitizenDataView().getCustomTextureUUID() == null);
    }
}
