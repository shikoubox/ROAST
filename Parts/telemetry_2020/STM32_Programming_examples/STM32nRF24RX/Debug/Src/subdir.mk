################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Src/main.c \
../Src/stm32f0xx_hal_msp.c \
../Src/stm32f0xx_it.c \
../Src/syscalls.c \
../Src/system_stm32f0xx.c 

OBJS += \
./Src/main.o \
./Src/stm32f0xx_hal_msp.o \
./Src/stm32f0xx_it.o \
./Src/syscalls.o \
./Src/system_stm32f0xx.o 

C_DEPS += \
./Src/main.d \
./Src/stm32f0xx_hal_msp.d \
./Src/stm32f0xx_it.d \
./Src/syscalls.d \
./Src/system_stm32f0xx.d 


# Each subdirectory must supply rules for building sources it contributes
Src/main.o: ../Src/main.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU GCC Compiler'
	@echo $(PWD)
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -mfloat-abi=soft -DUSE_HAL_DRIVER -DSTM32F042x6 -I"/home/bugi/STM32/Projects/STM32nRF24RX/Inc" -I"/home/bugi/STM32/Projects/STM32nRF24RX/Drivers/nRF24/Inc" -I"/home/bugi/STM32/Projects/STM32nRF24RX/Drivers/STM32F0xx_HAL_Driver/Inc" -I"/home/bugi/STM32/Projects/STM32nRF24RX/Drivers/STM32F0xx_HAL_Driver/Inc/Legacy" -I"/home/bugi/STM32/Projects/STM32nRF24RX/Drivers/CMSIS/Device/ST/STM32F0xx/Include" -I"/home/bugi/STM32/Projects/STM32nRF24RX/Drivers/CMSIS/Include"  -Og -g3 -Wall -fmessage-length=0 -ffunction-sections -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Src/%.o: ../Src/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU GCC Compiler'
	@echo $(PWD)
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -mfloat-abi=soft -DUSE_HAL_DRIVER -DSTM32F042x6 -I"/home/bugi/STM32/Projects/STM32nRF24RX/Inc" -I"/home/bugi/STM32/Projects/STM32nRF24RX/Drivers/STM32F0xx_HAL_Driver/Inc" -I"/home/bugi/STM32/Projects/STM32nRF24RX/Drivers/STM32F0xx_HAL_Driver/Inc/Legacy" -I"/home/bugi/STM32/Projects/STM32nRF24RX/Drivers/CMSIS/Device/ST/STM32F0xx/Include" -I"/home/bugi/STM32/Projects/STM32nRF24RX/Drivers/CMSIS/Include"  -Og -g3 -Wall -fmessage-length=0 -ffunction-sections -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


